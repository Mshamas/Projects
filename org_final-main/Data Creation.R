library(tidyverse)
library(arrow)
library(tidyverse)
library(lubridate)
library(gender)
library(igraph)
library(dplyr)


# Read the data
applications <- read_parquet("/Users/kaz/DataspellProjects/Org-Analytics/E3/app_data_sample.parquet")
edges <- read_csv("/Users/kaz/DataspellProjects/Org-Analytics/E3/edges_sample.csv")


# ---------------Get Tenure---------------
examiner_dates <- applications %>%
  select(examiner_id, filing_date, appl_status_date)

examiner_dates <- examiner_dates %>%
  mutate(start_date = ymd(filing_date), end_date = as_date(dmy_hms(appl_status_date)))

examiner_dates <- examiner_dates %>%
  group_by(examiner_id) %>%
  summarise(
    earliest_date = min(start_date, na.rm = TRUE),
    latest_date = max(end_date, na.rm = TRUE),
    tenure_days = interval(earliest_date, latest_date) %/% days(1)
  ) %>%
  filter(year(latest_date)<2018)

applications <- applications %>%
  left_join(examiner_dates, by = "examiner_id")

rm(examiner_dates)
gc()

# ---------------Get Status Year---------------
applications <- applications %>% mutate(end_date = as_date(dmy_hms(appl_status_date)))
applications <- applications %>% mutate(status_year = year(end_date))

applications <- applications %>% filter(status_year <= 2017)

#  ---------- filing year -------------
applications <- applications %>% mutate(filing_year = year(filing_date))



# ----------------- Gender Var,  -----------------
library(gender)
examiner_names <- applications %>%
  distinct(examiner_name_first)

examiner_names_gender <- examiner_names %>%
  do(results = gender(.$examiner_name_first, method = "ssa")) %>%
  unnest(cols = c(results), keep_empty = TRUE) %>%
  select(
    examiner_name_first = name,
    gender,
    proportion_female)

# remove extra colums from the gender table
examiner_names_gender <- examiner_names_gender %>%
  select(examiner_name_first, gender)

# joining gender back to the dataset
applications <- applications %>%
  left_join(examiner_names_gender, by = "examiner_name_first")

# cleaning up
rm(examiner_names)
rm(examiner_names_gender)
gc()

# ----------------- Ethnicity Var -----------------
library(wru)

examiner_surnames <- applications %>%
  select(surname = examiner_name_last) %>%
  distinct()

examiner_race <- predict_race(voter.file = examiner_surnames, surname.only = T) %>%
  as_tibble()

examiner_race <- examiner_race %>%
  mutate(max_race_p = pmax(pred.asi, pred.bla, pred.his, pred.oth, pred.whi)) %>%
  mutate(race = case_when(
    max_race_p == pred.asi ~ "Asian",
    max_race_p == pred.bla ~ "black",
    max_race_p == pred.his ~ "Hispanic",
    max_race_p == pred.oth ~ "other",
    max_race_p == pred.whi ~ "white",
    TRUE ~ NA_character_
  ))



# removing extra columns
examiner_race <- examiner_race %>%
  select(surname,race)

applications <- applications %>%
  left_join(examiner_race, by = c("examiner_name_last" = "surname"))

rm(examiner_race)
rm(examiner_surnames)
gc()

# ----------------- Create Work Group -----------------
# create a workgroup variable (first 3 digits of art unit
applications<- applications %>%
  mutate(
    workgroup = substr(examiner_art_unit, 1, 3)
  )


# ----------------- Create Graph -----------------
advice_network <- graph_from_data_frame(d = edges[, c("ego_examiner_id", "alter_examiner_id")], directed = TRUE)

# Create the induced subgraph
largest_subgraph <- components(advice_network)$membership == which.max(sizes(components(advice_network)))
largest_advice_network <- induced_subgraph(advice_network, largest_subgraph)

in_degree_centrality <- degree(largest_advice_network, mode = "in") # in-degree centrality
out_degree_centrality <- degree(largest_advice_network, mode = "out")
betweenness_centrality <- betweenness(largest_advice_network, directed = TRUE)

centrality_scores <- data.frame(
  examiner_id = V(largest_advice_network)$name,
  in_degree = in_degree_centrality,
  out_degree = out_degree_centrality,
  betweenness = betweenness_centrality
)



#### ----- Join the centrality scores to the applications dataset -------
# uniaue application numbers
edges_unique_applications <- edges %>% distinct(application_number) %>% pull(application_number)
length(edges_unique_applications)

# filter the applications that are in the advice network - row
applications_2008 <- applications %>% filter(application_number %in% edges_unique_applications)

applications_2008$examiner_id <- as.character(applications_2008$examiner_id)
centrality_scores$examiner_id <- as.character(centrality_scores$examiner_id)

# merge the centrality scores with the applications data
applications_2008 <- applications_2008 %>%
  left_join(centrality_scores, by = "examiner_id")


# ----------------- Save the Data-----------------
applications_w_ntrkScores <- applications_2008

write_csv(applications_w_ntrkScores, "applications_w_ntrkScores.csv")
write_csv(applications, "applications.csv")








# ----------------- Creating Data from the Transaction data  -----------------
# ----------------- Creating Data from the Transaction data  -----------------
# ----------------- Creating Data from the Transaction data  -----------------


# Load necessary libraries
library(dplyr)
library(lubridate)
library(readr)

# Read edge data and compute advice counts
edges <- read_csv('E3/edges_sample.csv')
advice_counts <- edges %>%
  group_by(application_number, advice_date) %>%
  summarise(advice_count = n(), .groups = 'drop')

# Read transactions data and merge with advice counts
transactions <- read_csv('../../Desktop/Final Project/Data/transactions_filtered.csv')
transactions <- transactions %>%
  left_join(advice_counts, by = 'application_number') %>%
  filter(recorded_date == advice_date)

# Sort and filter transactions by event codes of interest
final_transactions <- transactions %>%
  arrange(application_number, sequence_number) %>%
  filter(event_code %in% c('MN/=', 'MCTNF', 'MCTFR'))

# Merge transactions to find the closest 'DOCK' event
merged_transactions <- merge(final_transactions, transactions, by = 'application_number', suffix = c('_final', '_orig'))
merged_transactions <- merged_transactions %>%
  filter(event_code_orig == 'DOCK', recorded_date_orig < recorded_date_final) %>%
  arrange(application_number, desc(recorded_date_orig)) %>%
  distinct(application_number, .keep_all = TRUE)

# Calculate processing time and sequence difference
merged_transactions <- merged_transactions %>%
  mutate(
    recorded_date_final = as.Date(recorded_date_final),
    recorded_date_orig = as.Date(recorded_date_orig),
    processing_time = as.integer(difftime(recorded_date_final, recorded_date_orig, units = "days")),
    sequence_diff = sequence_number_final - sequence_number_orig,
    avg_processing_time = processing_time / sequence_diff
  )

# Load application data
applications <- read_csv('../../Desktop/Final Project/Data/applications_w_ntrkScores.csv')
applications <- applications %>%
  select(application_number, examiner_id, workgroup, uspc_class, tc, earliest_date, gender, race, in_degree, out_degree, betweenness)

# Merge closest dock events with application data
closest_dock_events <- merge(merged_transactions, applications, by = 'application_number', all.x = TRUE)
closest_dock_events <- closest_dock_events %>%
  mutate(
    earliest_date = as.Date(earliest_date),
    experience = as.integer(difftime(start_date, earliest_date, units = "days"))
  )

# Save the final dataset
# write_csv(closest_dock_events, 'Final Project/Data/closest_dock_events.csv')
