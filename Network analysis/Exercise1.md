## Required Libraries

    library(dplyr)

    ## Warning: package 'dplyr' was built under R version 4.2.3

    ## 
    ## Attaching package: 'dplyr'

    ## The following objects are masked from 'package:stats':
    ## 
    ##     filter, lag

    ## The following objects are masked from 'package:base':
    ## 
    ##     intersect, setdiff, setequal, union

    library(stringr)

    ## Warning: package 'stringr' was built under R version 4.2.3

    library(tidyr)

    ## Warning: package 'tidyr' was built under R version 4.2.3

    library(igraph)

    ## Warning: package 'igraph' was built under R version 4.2.3

    ## 
    ## Attaching package: 'igraph'

    ## The following object is masked from 'package:tidyr':
    ## 
    ##     crossing

    ## The following objects are masked from 'package:dplyr':
    ## 
    ##     as_data_frame, groups, union

    ## The following objects are masked from 'package:stats':
    ## 
    ##     decompose, spectrum

    ## The following object is masked from 'package:base':
    ## 
    ##     union

    library(readr)

    ## Warning: package 'readr' was built under R version 4.2.3

## Reading LinkedIn Data

    linkedin_data <- read_csv("C:/Users/m_sha/Downloads/Basic_LinkedInDataExport_03-14-2024/Connections.csv", 
                              skip = 3)

    ## Rows: 385 Columns: 7
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr (7): First Name, Last Name, URL, Email Address, Company, Position, Conne...
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

## Analyzing Contacts by Their Current Company

    company_contact_counts <- linkedin_data %>%
      group_by(Company) %>%
      summarise(Count = n()) %>%
      arrange(desc(Count))

    print(company_contact_counts)

    ## # A tibble: 245 × 2
    ##    Company                                             Count
    ##    <chr>                                               <int>
    ##  1 McGill University - Desautels Faculty of Management    22
    ##  2 McGill University                                      14
    ##  3 TD                                                     10
    ##  4 Pratt & Whitney Canada                                  7
    ##  5 <NA>                                                    7
    ##  6 CAE                                                     6
    ##  7 Desautels Capital Management                            6
    ##  8 Sunnybrook                                              6
    ##  9 CN                                                      5
    ## 10 L'Oréal                                                 5
    ## # ℹ 235 more rows

## Calculating the Total Number of Contacts

    total_contacts <- sum(company_contact_counts$Count)
    print(paste("Total contacts:", total_contacts))

    ## [1] "Total contacts: 385"

## Preparing Data for Network Analysis

### Generating Unique Names for Nodes

    linkedin_data$NodeName <- with(linkedin_data, paste(`First Name`, substring(`Last Name`, 1, 1), sep = "_"))

### Adding Unique Identifiers

    linkedin_data <- linkedin_data %>%
      mutate(NodeID = row_number())

### Creating Unique Nodes

    nodes_unique <- linkedin_data %>%
      distinct(NodeID, NodeName, Company)

### Preparing Data for Connections Between Nodes

    edges_for_analysis <- linkedin_data %>%
      inner_join(nodes_unique, by = c("NodeName", "Company"))

### Identifying Connections Between Individuals Within the Same Company

    connections_details <- nodes_unique %>%
      group_by(Company) %>%
      filter(n() > 1) %>%
      summarise(CombinationPairs = list(combn(NodeID, 2, simplify = FALSE))) %>%
      unnest(CombinationPairs) %>%
      ungroup() %>%
      mutate(From = sapply(CombinationPairs, `[`, 1),
             To = sapply(CombinationPairs, `[`, 2)) %>%
      select(From, To)

    print(connections_details)

    ## # A tibble: 563 × 2
    ##     From    To
    ##    <int> <int>
    ##  1    54    58
    ##  2    54   297
    ##  3    58   297
    ##  4   183   189
    ##  5   255   318
    ##  6   255   328
    ##  7   318   328
    ##  8    52    64
    ##  9   167   228
    ## 10   167   317
    ## # ℹ 553 more rows

## Building and Plotting the Network Graph

    network_diagram <- graph_from_data_frame(d = connections_details, vertices = nodes_unique, directed = TRUE)
    plot(network_diagram, vertex.label = V(network_diagram)$NodeName)

![](Exercise1_files/figure-markdown_strict/network-graph-1.png)
