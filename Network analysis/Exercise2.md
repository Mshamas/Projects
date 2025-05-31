## Required Libraries

    library(igraph)

    ## Warning: package 'igraph' was built under R version 4.2.3

    ## 
    ## Attaching package: 'igraph'

    ## The following objects are masked from 'package:stats':
    ## 
    ##     decompose, spectrum

    ## The following object is masked from 'package:base':
    ## 
    ##     union

    library(ggplot2)

    ## Warning: package 'ggplot2' was built under R version 4.2.3

    library(ggraph)

    ## Warning: package 'ggraph' was built under R version 4.2.3

    library(dplyr)

    ## Warning: package 'dplyr' was built under R version 4.2.3

    ## 
    ## Attaching package: 'dplyr'

    ## The following objects are masked from 'package:igraph':
    ## 
    ##     as_data_frame, groups, union

    ## The following objects are masked from 'package:stats':
    ## 
    ##     filter, lag

    ## The following objects are masked from 'package:base':
    ## 
    ##     intersect, setdiff, setequal, union

## Reading Fakebook Bus Data

    edges <- read.csv("C:/Users/m_sha/Documents/ONA Assignments/2024-ona-assignments/fakebook_bus_edges.csv")

## Create a graph from the edge list

    g <- graph_from_data_frame(edges, directed = FALSE)

## Centrality measures

    # Calculate centrality measures
    degree_centrality <- degree(g) / (vcount(g) - 1)
    closeness_centrality <- closeness(g)
    betweenness_centrality <- betweenness(g)

    # Create a data frame that includes centrality measures
    centrality_df <- data.frame(node=names(degree_centrality),
                                degree=degree_centrality,
                                closeness=closeness_centrality,
                                betweenness=betweenness_centrality)

    # Add centrality measures to the graph object as attributes
    V(g)$degree <- centrality_df$degree
    V(g)$closeness <- centrality_df$closeness
    V(g)$betweenness <- centrality_df$betweenness

## Node colours and labels

    # Define node colors based on seat type
    V(g)$color <- ifelse(V(g)$name %in% c('1', '2', '3', '4', '5', '6'), 'red', 'green')

    # Create a label for each node with seat number and centrality measures for open seats
    V(g)$label <- ifelse(V(g)$name %in% c('A', 'B', 'C', 'D'),
                         paste(V(g)$name,
                               "\nDeg:", round(V(g)$degree, 2), 
                               "\nClose:", round(V(g)$closeness, 2),
                               "\nBetween:", round(V(g)$betweenness, 2), sep=""),
                         V(g)$name)

## Plot final graph

    ggraph(g, layout = 'fr') + 
      geom_edge_link(edge_width = 1, edge_colour = "grey") +
      geom_node_point(aes(size = degree, color = color), show.legend = TRUE) +
      geom_node_text(aes(label = label), repel = TRUE, 
                     point.padding = unit(0.75, "lines"),
                     nudge_x = 0.05, nudge_y = 0.1, 
                     color = "black") +
      theme_void() +
      ggtitle("Fakebook Bus Network Graph with Centrality Measures") +
      scale_color_manual(values = c('red' = 'red', 'green' = 'green'))

![](Exercise2_files/figure-markdown_strict/final%20graph-1.png)

Seat Analysis:

Seat A Analysis: Choosing Seat A may lead to limited interaction
opportunities due to its lower centrality metrics. It is less central in
terms of both the number of direct connections (degree) and its
proximity to all other nodes in the network (closeness), and it seldom
acts as a bridge (betweenness). For those aiming to maximize their
interactions, Seat A might not be the optimal choice.

Seat B Analysis: Seat B stands out for its potential for greater direct
interactions, evidenced by higher degree and betweenness centrality
values compared to Seat A. It acts more frequently as a bridge within
the network, making it an appealing option for individuals looking to
serve as connectors or hubs of interaction.

Seat C Analysis: Seat C is the prime choice for maximizing interaction
potential, characterized by the highest closeness centrality. This
indicates it is, on average, closest to all other nodes, facilitating
more rapid and frequent connections. Its significant betweenness
centrality further highlights its role as a crucial junction within the
network, ideal for those keen on establishing broad connections.

Seat D Analysis: Although Seat D offers a better potential for
interaction compared to Seat A, it still falls short of Seats B and C.
Its somewhat higher closeness and betweenness centrality suggest a
moderate level of interaction potential, positioning it as a viable
option for those seeking a balance between engagement and a peaceful
journey.

Conclusion: Selecting Seat C appears most beneficial for those aiming to
be at the center of interactions, likely enhancing the chance of
engaging with a wide array of individuals. This choice is well-suited
for objectives centered around networking and expanding social circles.
