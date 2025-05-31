### Load the libraries

    library(tidyverse)

    ## Warning: package 'ggplot2' was built under R version 4.3.1

    ## Warning: package 'lubridate' was built under R version 4.3.1

    ## ── Attaching core tidyverse packages ──────────────────────── tidyverse 2.0.0 ──
    ## ✔ dplyr     1.1.2     ✔ readr     2.1.4
    ## ✔ forcats   1.0.0     ✔ stringr   1.5.0
    ## ✔ ggplot2   3.5.0     ✔ tibble    3.2.1
    ## ✔ lubridate 1.9.3     ✔ tidyr     1.3.0
    ## ✔ purrr     1.0.1     
    ## ── Conflicts ────────────────────────────────────────── tidyverse_conflicts() ──
    ## ✖ dplyr::filter() masks stats::filter()
    ## ✖ dplyr::lag()    masks stats::lag()
    ## ℹ Use the conflicted package (<http://conflicted.r-lib.org/>) to force all conflicts to become errors

    library(arrow)

    ## Warning: package 'arrow' was built under R version 4.3.1

    ## 
    ## Attaching package: 'arrow'
    ## 
    ## The following object is masked from 'package:lubridate':
    ## 
    ##     duration
    ## 
    ## The following object is masked from 'package:utils':
    ## 
    ##     timestamp

    library(tidyverse)
    library(lubridate)
    library(gender)
    library(igraph)

    ## Warning: package 'igraph' was built under R version 4.3.1

    ## 
    ## Attaching package: 'igraph'
    ## 
    ## The following objects are masked from 'package:lubridate':
    ## 
    ##     %--%, union
    ## 
    ## The following objects are masked from 'package:dplyr':
    ## 
    ##     as_data_frame, groups, union
    ## 
    ## The following objects are masked from 'package:purrr':
    ## 
    ##     compose, simplify
    ## 
    ## The following object is masked from 'package:tidyr':
    ## 
    ##     crossing
    ## 
    ## The following object is masked from 'package:tibble':
    ## 
    ##     as_data_frame
    ## 
    ## The following objects are masked from 'package:stats':
    ## 
    ##     decompose, spectrum
    ## 
    ## The following object is masked from 'package:base':
    ## 
    ##     union

    library(dplyr)

### Load the data - this is filtered & merged (with transaction) data

    applications <- read.csv("/Users/kaz/Desktop/Final Project_org/Data/closest_dock_events.csv")

### Experience Variable

This variable is a measure of the number of years of experience of the
applicant. It is calculated by subtracting the year of the “filing” from
the year of the first publication of the applicant.

    # distribution of experience
    ggplot(applications, aes(x = experience)) +
      geom_histogram(fill = "skyblue", color = "black", bins = 100) +
      labs(title = "Distribution of Experience",
           x = "Experience (days)",
           y = "Frequency")

    ## Warning: Removed 39 rows containing non-finite outside the scale range
    ## (`stat_bin()`).

![](/Users/kaz/DataspellProjects/org_final/EDA_files/figure-markdown_strict/unnamed-chunk-3-1.png)

    # experience by race gender and race
    # distinct examiner_id and keep all columns
    applications_unique <- applications %>% distinct(application_number, .keep_all = TRUE)

    library(RColorBrewer)

    ggplot(applications_unique, aes(x = gender, y = experience, fill = race)) +
      geom_boxplot() +
      scale_fill_brewer(palette = "Paired") +  # You can choose other palettes like "Dark2", "Set3", etc.
      labs(title = "Distribution of Experience by Gender and Race",
           x = "Gender",
           y = "Experience") +
      theme_minimal() +
      theme(axis.text.x = element_text(angle = 45, hjust = 1))  # Adjust text angle if needed

    ## Warning: Removed 39 rows containing non-finite outside the scale range
    ## (`stat_boxplot()`).

![](/Users/kaz/DataspellProjects/org_final/EDA_files/figure-markdown_strict/unnamed-chunk-4-1.png)

    # create experience_year variable - floor the experience to years
    applications$experience_years <- floor(applications$experience / 365)

### how does network feature vary by seniority (experience)

    ggplot(applications, aes(x = gender, y = processing_time, fill = race)) +
      geom_boxplot() +
      scale_fill_brewer(palette = "Paired") +  # You can choose other palettes like "Dark2", "Set3", etc.
      labs(title = "Distribution of Processing Time by Gender and Race",
           x = "Gender",
           y = "Processing Time (days)") +
      theme_minimal() +
      theme(axis.text.x = element_text(angle = 45, hjust = 1))  # Adjust text angle if needed

![](/Users/kaz/DataspellProjects/org_final/EDA_files/figure-markdown_strict/unnamed-chunk-6-1.png)

    # Create the boxplot without displaying outliers and limit y-axis to 50
    ggplot(applications, aes(x = as.factor(experience_years), y = in_degree, color = experience)) +
      geom_boxplot(outlier.shape = NA) +  # This hides outliers
      labs(title = "Boxplot of In-Degree by Experience", x = "Experience", y = "In-Degree") +
      theme_minimal() +
      scale_y_continuous(limits = c(0, 20))  # Limit y-axis to 0 to 50

    ## Warning: Removed 2655 rows containing non-finite outside the scale range
    ## (`stat_boxplot()`).

    ## Warning: The following aesthetics were dropped during statistical transformation:
    ## colour.
    ## ℹ This can happen when ggplot fails to infer the correct grouping structure in
    ##   the data.
    ## ℹ Did you forget to specify a `group` aesthetic or to convert a numerical
    ##   variable into a factor?

![](/Users/kaz/DataspellProjects/org_final/EDA_files/figure-markdown_strict/unnamed-chunk-7-1.png)

    # Create the boxplot using 'race' for x-axis and 'experience_years' to differentiate within each boxplot
    ggplot(applications, aes(x = as.factor(gender), y = in_degree, fill = as.factor(experience_years))) +
      geom_boxplot(outlier.shape = NA) +  # This hides outliers
      scale_fill_brewer(palette = "Paired") +  # Use a color palette that provides clear differentiation
      labs(title = "Boxplot of In-Degree by Genger and Experience Years",
           x = "Gender",
           y = "In-Degree") +
      theme_minimal() +
      scale_y_continuous(limits = c(0, 20)) +  # Limit y-axis to 0 to 20 for clarity
      theme(legend.position = "bottom")  # Adjust legend position to avoid clutter

    ## Warning: Removed 2655 rows containing non-finite outside the scale range
    ## (`stat_boxplot()`).

![](/Users/kaz/DataspellProjects/org_final/EDA_files/figure-markdown_strict/unnamed-chunk-8-1.png)

    # Create the boxplot using 'race' for x-axis and 'experience_years' to differentiate within each boxplot
    ggplot(applications, aes(x = as.factor(gender), y = out_degree, fill = as.factor(experience_years))) +
      geom_boxplot(outlier.shape = NA) +  # This hides outliers
      scale_fill_brewer(palette = "Paired") +  # Use a color palette that provides clear differentiation
      labs(title = "Boxplot of Out-Degree by Genger and Experience Years",
           x = "Gender",
           y = "Out-Degree") +
      theme_minimal() +
      scale_y_continuous(limits = c(0, 20)) +  # Limit y-axis to 0 to 20 for clarity
      theme(legend.position = "bottom")  # Adjust legend position to avoid clutter

    ## Warning: Removed 8550 rows containing non-finite outside the scale range
    ## (`stat_boxplot()`).

![](/Users/kaz/DataspellProjects/org_final/EDA_files/figure-markdown_strict/unnamed-chunk-9-1.png)

**Mean Proc Time by workgroup and show distribution of means**

    wg_means <- applications %>%
      group_by(workgroup) %>%
      summarise(mean_proc_time=mean(processing_time, na.rm = TRUE),
                n = n()) %>% arrange(desc(mean_proc_time))

    # sort it
    ggplot(wg_means, aes(x = reorder(workgroup, mean_proc_time), y = mean_proc_time)) +
      geom_bar(stat = "identity", fill = "skyblue", color = "black") +
      labs(title = "Mean Processing Time by Workgroup",
           x = "Workgroup",
           y = "Mean Processing Time (days)") +
      theme(axis.text.x = element_text(angle = 45, hjust = 1))

![](/Users/kaz/DataspellProjects/org_final/EDA_files/figure-markdown_strict/unnamed-chunk-10-1.png)

**Application Status is limited to 150 and 161**

    applications %>%
      group_by(gender) %>%
      summarise(mean_app_proc_time=mean(processing_time, na.rm = TRUE),
                n = n()) %>% arrange(desc(n))

    ## # A tibble: 3 × 3
    ##   gender   mean_app_proc_time     n
    ##   <chr>                 <dbl> <int>
    ## 1 "male"                 201.  8214
    ## 2 "female"               255.  3516
    ## 3 ""                     235.  2538

    applications %>%
      group_by(race) %>%
      summarise(mean_app_proc_time=mean(processing_time, na.rm = TRUE),
                n = n()) %>% arrange(desc(n))

    ## # A tibble: 5 × 3
    ##   race     mean_app_proc_time     n
    ##   <chr>                 <dbl> <int>
    ## 1 white                  225.  7831
    ## 2 Asian                  218.  5502
    ## 3 black                  211.   513
    ## 4 Hispanic               193.   381
    ## 5 other                  145.    41

<table>
<colgroup>
<col style="width: 7%" />
<col style="width: 67%" />
<col style="width: 13%" />
<col style="width: 11%" />
</colgroup>
<thead>
<tr class="header">
<th>Code</th>
<th>Status</th>
<th>Frequency</th>
<th>Percent</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>150</td>
<td>Patented Case</td>
<td>4,288,187</td>
<td>46.5%</td>
</tr>
<tr class="even">
<td>161</td>
<td>Abandoned – Failure to Respond to an Office Action</td>
<td>1,107,772</td>
<td>12.0%</td>
</tr>
<tr class="odd">
<td>250</td>
<td>Patent Expired Due to NonPayment of Maintenance Fees Under 37 CFR
1.362</td>
<td>919,203</td>
<td>10.0%</td>
</tr>
<tr class="even">
<td>159</td>
<td>Provisional Application Expired</td>
<td>848,536</td>
<td>9.2%</td>
</tr>
<tr class="odd">
<td>30</td>
<td>Docketed New Case - Ready for Examination</td>
<td>350,347</td>
<td>3.8%</td>
</tr>
<tr class="even">
<td>218</td>
<td>RO PROCESSING COMPLETED-PLACED IN STORAGE</td>
<td>284,700</td>
<td>3.1%</td>
</tr>
<tr class="odd">
<td>566</td>
<td>PCT - International Search Report Mailed to IB</td>
<td>234,837</td>
<td>2.5%</td>
</tr>
<tr class="even">
<td>41</td>
<td>Non Final Action Mailed</td>
<td>168,103</td>
<td>1.8%</td>
</tr>
<tr class="odd">
<td>166</td>
<td>Abandoned – File-Wrapper-Continuation Parent Application</td>
<td>165,589</td>
<td>1.8%</td>
</tr>
<tr class="even">
<td>19</td>
<td>Application Undergoing Preexam Processing</td>
<td>126,741</td>
<td>1.4%</td>
</tr>
<tr class="odd">
<td>N/A</td>
<td>Other Codes</td>
<td>709,623</td>
<td>7.7%</td>
</tr>
<tr class="even">
<td></td>
<td>Missing</td>
<td>27,532</td>
<td>0.3%</td>
</tr>
<tr class="odd">
<td></td>
<td>Total</td>
<td>9,231,170</td>
<td>100.0%</td>
</tr>
</tbody>
</table>

#### Sequence diff vs processing\_time

    # Generate scatter plot of sequence_diff vs processing_time
    ggplot(applications, aes(x = sequence_diff, y = processing_time)) +
      geom_point(alpha = 0.5) +  # alpha for transparency if many points overlap
      labs(x = "Sequence Difference", y = "Processing Time",
           title = "Scatter Plot of Sequence Difference vs Processing Time") +
      theme_minimal()  # A clean theme for the plot

![](/Users/kaz/DataspellProjects/org_final/EDA_files/figure-markdown_strict/unnamed-chunk-12-1.png)

    ggplot(applications, aes(x = out_degree, y = processing_time)) +
      geom_point(alpha = 0.5) +  # alpha for transparency if many points overlap
      labs(x = "out_degree", y = "Processing Time",
           title = "Scatter Plot of out_deg vs Processing Time") +
      theme_minimal()  # A clean theme for the plot

    ## Warning: Removed 1320 rows containing missing values or values outside the scale range
    ## (`geom_point()`).

![](/Users/kaz/DataspellProjects/org_final/EDA_files/figure-markdown_strict/unnamed-chunk-13-1.png)

    ggplot(applications, aes(x = out_degree, y = processing_time)) +
      geom_point(alpha = 0.5) +  # alpha for transparency if many points overlap
      labs(x = "in_degree", y = "Processing Time",
           title = "Scatter Plot of out_deg vs Processing Time") +
      theme_minimal()  # A clean theme for the plot

    ## Warning: Removed 1320 rows containing missing values or values outside the scale range
    ## (`geom_point()`).

![](/Users/kaz/DataspellProjects/org_final/EDA_files/figure-markdown_strict/unnamed-chunk-14-1.png)

    ggplot(applications, aes(x = betweenness, y = processing_time)) +
      geom_point(alpha = 0.5) +  # alpha for transparency if many points overlap
      labs(x = "betweenness", y = "Processing Time",
           title = "Scatter Plot of between vs Processing Time") +
      theme_minimal()  # A clean theme for the plot

    ## Warning: Removed 1320 rows containing missing values or values outside the scale range
    ## (`geom_point()`).

![](/Users/kaz/DataspellProjects/org_final/EDA_files/figure-markdown_strict/unnamed-chunk-15-1.png)

    ggplot(applications, aes(x = advice_count_final)) +
      geom_histogram(fill = "skyblue", color = "black", bins = 100) +
      labs(title = "Distribution of Experience",
           x = "advice_counts",
           y = "Frequency")

![](/Users/kaz/DataspellProjects/org_final/EDA_files/figure-markdown_strict/unnamed-chunk-16-1.png)

### Adivce Network Visualization

    edges <- read.csv("/Users/kaz/Desktop/Final Project_org/Data/edges_sample.csv")
    advice_network <- graph_from_data_frame(d = edges[, c("ego_examiner_id", "alter_examiner_id")], directed = TRUE)

    ## Warning in graph_from_data_frame(d = edges[, c("ego_examiner_id",
    ## "alter_examiner_id")], : In `d' `NA' elements were replaced with string "NA"

    # value count gender in applications
    table(applications$gender)

    ## 
    ##        female   male 
    ##   2538   3516   8214

    # convert the "" to NA
    applications$gender[applications$gender == ""] <- "NA"
    table(applications$gender)

    ## 
    ##     NA female   male 
    ##   2538   3516   8214

    # Convert identifiers to character to avoid issues with factors
    edges$ego_examiner_id <- as.character(edges$ego_examiner_id)
    edges$alter_examiner_id <- as.character(edges$alter_examiner_id)
    applications$examiner_id <- as.character(applications$examiner_id)
    # Ensure applications have unique entries per examiner
    applications_unique <- applications %>% distinct(examiner_id, .keep_all = TRUE)

    ### Create the Advice Network
    advice_network <- graph_from_data_frame(d = edges[, c("ego_examiner_id", "alter_examiner_id")], directed = TRUE)

    ## Warning in graph_from_data_frame(d = edges[, c("ego_examiner_id",
    ## "alter_examiner_id")], : In `d' `NA' elements were replaced with string "NA"

    ### Merge Node Attributes
    # First, merge node attributes with the main network
    node_attributes <- merge(data.frame(id = V(advice_network)$name), applications_unique, by.x = "id", by.y = "examiner_id", all.x = TRUE)
    V(advice_network)$race <- node_attributes$race
    V(advice_network)$gender <- node_attributes$gender

    ### Analyze the Largest Subgraph
    # Identify the largest component
    largest_subgraph_members <- components(advice_network)$membership == which.max(sizes(components(advice_network)))

    # Create the induced subgraph for the largest component
    largest_advice_network <- induced_subgraph(advice_network, which(largest_subgraph_members))

    # Transfer and map attributes from the main network to the subgraph
    V(largest_advice_network)$gender <- V(advice_network)$gender[V(largest_advice_network)]
    V(largest_advice_network)$race <- V(advice_network)$race[V(largest_advice_network)]

    in_degree_centrality <- degree(largest_advice_network, mode = "in") # in-degree centrality
    out_degree_centrality <- degree(largest_advice_network, mode = "out")

    # Add out-degree centrality as a vertex attribute for visualization
    # Calculate betweenness centrality for each node (examiner)
    betweenness_centrality <- betweenness(largest_advice_network, directed = TRUE)

    V(largest_advice_network)$out_degree <- out_degree_centrality
    V(largest_advice_network)$in_degree <- in_degree_centrality
    V(largest_advice_network)$betweenness <- betweenness_centrality

    # Create a dataframe of centrality scores
    centrality_scores <- data.frame(
      examiner_id = V(largest_advice_network)$name,
      in_degree = in_degree_centrality,
      out_degree = out_degree_centrality,
      betweenness = betweenness_centrality
    )

    # Calculate means and standard deviations for in-degree and out-degree
    in_mean <- mean(degree(largest_advice_network, mode = "in"))
    in_sd <- sd(degree(largest_advice_network, mode = "in"))
    out_mean <- mean(degree(largest_advice_network, mode = "out"))
    out_sd <- sd(degree(largest_advice_network, mode = "out"))

    gender_colors <- c(male = "slateblue", female = "orange", "NA" = "gray")

    # Apply the color mapping
    V(largest_advice_network)$color <- gender_colors[V(largest_advice_network)$gender]


    png(filename = "Network_Visualization_Bet_by_Gender.png", width = 1600, height = 1600)

    # Plot the network
    plot(largest_advice_network,
         main = "Network Visualization, Size=Betweenness Centrality, Color=Gender",
         vertex.size = ifelse(betweenness(largest_advice_network, directed = TRUE) >
                                      quantile(betweenness(largest_advice_network, directed = TRUE), 0.75), 4, 1),
         vertex.label = NA,
         vertex.color = V(largest_advice_network)$color,  # Color by gender
         vertex.frame.color = NA,  # No outline for nodes
         edge.arrow.size = 0.1,
         edge.color = rgb(0.2, 0.2, 0.2, 0.1))  # Semi-transparent edges
    dev.off()

    ## quartz_off_screen 
    ##                 2

    race_colors <- c(
      white = "#F0E442",  # Light Yellow, good for contrast with dark colors
      black = "#000000",  # Black, offers strong contrast against lighter colors
      Asian = "#FFA500",  # Orange, vibrant and stands out well
      Hispanic = "#377EB8",  # Blue, a different shade to distinguish from other colors
      other = "#E41A1C"   # Red, distinct and easily noticeable
    )

    V(largest_advice_network)$color <- race_colors[V(largest_advice_network)$race]


    # Plot the network
    png(filename = "Network_Visualization_Bet_by_Race.png", width = 800, height = 800)
    plot(largest_advice_network,
         main = "Network Visualization by Race",
         vertex.size = ifelse(betweenness(largest_advice_network, directed = TRUE) >
                                quantile(betweenness(largest_advice_network, directed = TRUE), 0.75), 4, 1),
         vertex.label = NA,
         vertex.color = V(largest_advice_network)$color,  # Color by race
         vertex.frame.color = NA,  # No outline for nodes
         edge.arrow.size = 0.06,
         edge.color = rgb(0.2, 0.2, 0.2, 0.05))  # Semi-transparent edges
    dev.off()

    ## quartz_off_screen 
    ##                 2

    gender_colors <- c(male = "slateblue", female = "orange", "NA" = "gray")

    # Apply the color mapping
    V(largest_advice_network)$color <- gender_colors[V(largest_advice_network)$gender]


    png(filename = "Network_Visualization_by_Gender_indeg.png", width = 1600, height = 1600)

    # Plot the network
    plot(largest_advice_network,
         main = "Network Visualization, Size=In-degree Centrality, Color=Gender",
         vertex.size = ifelse(degree(largest_advice_network, mode = "in") >
                                quantile(degree(largest_advice_network, mode = "in"), 0.75), 4, 1),
         vertex.label = NA,
         vertex.color = V(largest_advice_network)$color,  # Color by gender
         vertex.frame.color = NA,  # No outline for nodes
         edge.arrow.size = 0.1,
         edge.color = rgb(0.2, 0.2, 0.2, 0.1))  # Semi-transparent edges
    dev.off()

    ## quartz_off_screen 
    ##                 2

    race_colors <- c(
      white = "#F0E442",  # Light Yellow, good for contrast with dark colors
      black = "#000000",  # Black, offers strong contrast against lighter colors
      Asian = "#FFA500",  # Orange, vibrant and stands out well
      Hispanic = "#377EB8",  # Blue, a different shade to distinguish from other colors
      other = "#E41A1C"   # Red, distinct and easily noticeable
    )

    V(largest_advice_network)$color <- race_colors[V(largest_advice_network)$race]


    # Plot the network
    png(filename = "Network_Visualization_by_Race_indeg.png", width = 800, height = 800)
    plot(largest_advice_network,
         main = "Network Visualization, Size=In-degree Centrality, Color=Race",
         vertex.size = ifelse(degree(largest_advice_network, mode = "in") >
                                quantile(degree(largest_advice_network, mode = "in"), 0.75), 4, 1),
         vertex.label = NA,
         vertex.color = V(largest_advice_network)$color,  # Color by race
         vertex.frame.color = NA,  # No outline for nodes
         edge.arrow.size = 0.06,
         edge.color = rgb(0.2, 0.2, 0.2, 0.05))  # Semi-transparent edges
    dev.off()

    ## quartz_off_screen 
    ##                 2
