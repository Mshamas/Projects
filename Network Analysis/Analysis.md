### load Packages

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

### Load Data

    applications <- read_csv("/Users/kaz/Desktop/Final Project_org/Data/closest_dock_events.csv")

    ## Rows: 14268 Columns: 19
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr   (3): disposal_type, gender, race
    ## dbl  (13): application_number, advice_count_final, processing_time, sequence...
    ## date  (3): end_date, start_date, earliest_date
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

    str(applications)

    ## spc_tbl_ [14,268 × 19] (S3: spec_tbl_df/tbl_df/tbl/data.frame)
    ##  $ application_number : num [1:14268] 9402488 9445135 9479304 9484331 9489652 ...
    ##  $ advice_count_final : num [1:14268] 3 3 4 3 2 5 3 1 1 2 ...
    ##  $ end_date           : Date[1:14268], format: "2008-11-17" "2008-08-21" ...
    ##  $ start_date         : Date[1:14268], format: "2005-06-28" "2008-02-26" ...
    ##  $ processing_time    : num [1:14268] 1238 177 13 15 1024 ...
    ##  $ sequence_diff      : num [1:14268] 66 7 9 8 52 17 43 64 9 8 ...
    ##  $ avg_processing_time: num [1:14268] 18.76 25.29 1.44 1.88 19.69 ...
    ##  $ disposal_type      : chr [1:14268] "approved" "rejected" "approved" "approved" ...
    ##  $ examiner_id        : num [1:14268] 84356 92953 61293 61519 67078 ...
    ##  $ workgroup          : num [1:14268] 165 242 243 163 219 241 244 214 246 244 ...
    ##  $ uspc_class         : num [1:14268] 435 725 380 435 709 370 709 709 370 709 ...
    ##  $ tc                 : num [1:14268] 1600 2400 2400 1600 2100 2400 2400 2100 2400 2400 ...
    ##  $ earliest_date      : Date[1:14268], format: "2000-01-05" "2000-01-20" ...
    ##  $ gender             : chr [1:14268] "male" "female" "female" "male" ...
    ##  $ race               : chr [1:14268] "white" "Asian" "white" "Asian" ...
    ##  $ in_degree          : num [1:14268] 5 0 1 4 1 0 2 2 0 2 ...
    ##  $ out_degree         : num [1:14268] 30 6 0 9 5 85 54 54 32 54 ...
    ##  $ betweenness        : num [1:14268] 4018 0 0 1955 2787 ...
    ##  $ experience         : num [1:14268] 2001 2959 3253 2927 1898 ...
    ##  - attr(*, "spec")=
    ##   .. cols(
    ##   ..   application_number = col_double(),
    ##   ..   advice_count_final = col_double(),
    ##   ..   end_date = col_date(format = ""),
    ##   ..   start_date = col_date(format = ""),
    ##   ..   processing_time = col_double(),
    ##   ..   sequence_diff = col_double(),
    ##   ..   avg_processing_time = col_double(),
    ##   ..   disposal_type = col_character(),
    ##   ..   examiner_id = col_double(),
    ##   ..   workgroup = col_double(),
    ##   ..   uspc_class = col_double(),
    ##   ..   tc = col_double(),
    ##   ..   earliest_date = col_date(format = ""),
    ##   ..   gender = col_character(),
    ##   ..   race = col_character(),
    ##   ..   in_degree = col_double(),
    ##   ..   out_degree = col_double(),
    ##   ..   betweenness = col_double(),
    ##   ..   experience = col_double()
    ##   .. )
    ##  - attr(*, "problems")=<externalptr>

### Add Start Year

    applications <- applications %>%
      mutate(
        start_year = year(earliest_date)
      )

### Remove the NA value

    applications <- applications %>%
      filter(!is.na(processing_time ))

#### Change the date format

    applications$gender <- as.factor(applications$gender)
    applications$race <- as.factor(applications$race)
    # applications$examiner_art_unit <- as.factor(applications$examiner_art_unit)
    applications$workgroup <- as.factor(applications$workgroup)
    applications$start_year <- as.factor(applications$start_year)
    applications$disposal_type <- as.factor(applications$disposal_type)
    applications$uspc_class <- as.factor(applications$uspc_class)

    # distribution of processing time numeric it first

    applications$processing_time <- as.numeric(applications$processing_time)
    applications$ln_processing_time <- log(applications$processing_time)

### Model Building

    library(caTools)
    library(MASS)

    ## Warning: package 'MASS' was built under R version 4.3.1

    ## 
    ## Attaching package: 'MASS'

    ## The following object is masked from 'package:dplyr':
    ## 
    ##     select

    library(lmtest)

    ## Loading required package: zoo

    ## 
    ## Attaching package: 'zoo'

    ## The following objects are masked from 'package:base':
    ## 
    ##     as.Date, as.Date.numeric

    set.seed(123)  # for reproducibility
    split <- sample.split(applications$processing_time, SplitRatio = 0.8)
    train_data <- subset(applications, split == TRUE)
    test_data <- subset(applications, split == FALSE)

### Dealing with NA

    # Remove rows with any missing value
    train_data <- na.omit(train_data)
    test_data <- na.omit(test_data)

    # model <- lm(processing_time ~  gender + race + experience + in_degree + out_degree + betweenness + disposal_type + sequence_diff + advice_count_final + start_year + workgroup,
    #             data = train_data)

    model <- lm(processing_time ~  gender + race + experience + in_degree + out_degree + betweenness + disposal_type  + advice_count_final + start_year + workgroup,
                data = train_data)

    model2 <- lm(processing_time ~ gender * in_degree + gender * out_degree + gender * betweenness +
            race * in_degree + race * out_degree + race * betweenness +
            experience + disposal_type + advice_count_final + start_year + workgroup,
                data = train_data)

    # model <- lm(avg_processing_time ~  gender + race + experience + in_degree + out_degree + betweenness + disposal_type + sequence_diff + advice_count_final + start_year + workgroup,
    #             data = applications)

    library(stargazer)

    ## 
    ## Please cite as:

    ##  Hlavac, Marek (2022). stargazer: Well-Formatted Regression and Summary Statistics Tables.

    ##  R package version 5.2.3. https://CRAN.R-project.org/package=stargazer

    # Using stargazer to generate an HTML table of the model summary
    summary(model)

    ## 
    ## Call:
    ## lm(formula = processing_time ~ gender + race + experience + in_degree + 
    ##     out_degree + betweenness + disposal_type + advice_count_final + 
    ##     start_year + workgroup, data = train_data)
    ## 
    ## Residuals:
    ##     Min      1Q  Median      3Q     Max 
    ## -447.58  -82.78   -0.89   83.41  564.65 
    ## 
    ## Coefficients:
    ##                         Estimate Std. Error  t value Pr(>|t|)    
    ## (Intercept)            2.521e+03  1.407e+01  179.159  < 2e-16 ***
    ## gendermale            -1.303e+01  3.171e+00   -4.110 3.99e-05 ***
    ## raceHispanic           1.173e+01  8.367e+00    1.401 0.161108    
    ## raceblack              2.260e+01  7.757e+00    2.914 0.003579 ** 
    ## raceother              9.802e+01  4.162e+01    2.355 0.018536 *  
    ## racewhite             -9.384e+00  3.164e+00   -2.966 0.003028 ** 
    ## experience            -7.949e-01  4.520e-03 -175.862  < 2e-16 ***
    ## in_degree              3.663e-02  7.907e-02    0.463 0.643161    
    ## out_degree             9.935e-02  3.306e-02    3.005 0.002662 ** 
    ## betweenness            8.692e-04  1.405e-04    6.185 6.51e-10 ***
    ## disposal_typerejected -1.443e+01  3.665e+00   -3.938 8.29e-05 ***
    ## advice_count_final    -1.834e+00  6.092e-01   -3.011 0.002613 ** 
    ## start_year2001        -3.369e+02  4.470e+00  -75.366  < 2e-16 ***
    ## start_year2002        -6.287e+02  5.457e+00 -115.198  < 2e-16 ***
    ## start_year2003        -9.534e+02  6.456e+00 -147.672  < 2e-16 ***
    ## start_year2004        -1.219e+03  7.575e+00 -160.868  < 2e-16 ***
    ## start_year2005        -1.459e+03  1.015e+01 -143.773  < 2e-16 ***
    ## start_year2006        -1.682e+03  1.685e+01  -99.860  < 2e-16 ***
    ## workgroup162          -1.207e+00  1.657e+01   -0.073 0.941922    
    ## workgroup163           6.513e+01  1.480e+01    4.402 1.09e-05 ***
    ## workgroup164           2.665e+01  9.496e+00    2.806 0.005027 ** 
    ## workgroup165           1.238e+01  1.204e+01    1.029 0.303736    
    ## workgroup166           7.525e+01  5.572e+01    1.351 0.176852    
    ## workgroup167          -2.144e+01  2.802e+01   -0.765 0.444228    
    ## workgroup171          -9.731e+00  1.504e+01   -0.647 0.517638    
    ## workgroup172          -4.941e+01  1.676e+01   -2.948 0.003212 ** 
    ## workgroup173          -4.724e+01  2.121e+01   -2.227 0.025941 *  
    ## workgroup174          -1.083e+01  2.203e+01   -0.492 0.623062    
    ## workgroup175          -1.393e+02  7.176e+01   -1.941 0.052303 .  
    ## workgroup176          -1.438e+01  1.761e+01   -0.817 0.414127    
    ## workgroup177          -1.257e+01  1.814e+01   -0.693 0.488432    
    ## workgroup178          -2.452e+01  1.440e+01   -1.703 0.088603 .  
    ## workgroup179          -3.221e+01  7.895e+00   -4.080 4.55e-05 ***
    ## workgroup211          -4.678e+01  1.022e+01   -4.576 4.81e-06 ***
    ## workgroup212          -6.194e+01  1.097e+01   -5.648 1.68e-08 ***
    ## workgroup213          -7.791e+01  1.496e+01   -5.209 1.94e-07 ***
    ## workgroup214          -4.797e+01  1.566e+01   -3.063 0.002202 ** 
    ## workgroup215          -1.040e+02  1.007e+01  -10.327  < 2e-16 ***
    ## workgroup216          -6.697e+01  8.978e+00   -7.459 9.57e-14 ***
    ## workgroup217          -5.456e+01  1.239e+01   -4.402 1.09e-05 ***
    ## workgroup218          -8.008e+01  1.012e+01   -7.910 2.89e-15 ***
    ## workgroup219          -5.367e+01  1.185e+01   -4.530 5.97e-06 ***
    ## workgroup241          -5.048e+01  9.208e+00   -5.482 4.32e-08 ***
    ## workgroup242          -6.654e+01  9.263e+00   -7.184 7.37e-13 ***
    ## workgroup243          -6.125e+01  1.219e+01   -5.023 5.19e-07 ***
    ## workgroup244          -6.468e+01  9.368e+00   -6.905 5.40e-12 ***
    ## workgroup245          -4.342e+01  9.249e+00   -4.694 2.72e-06 ***
    ## workgroup246          -5.275e+01  1.049e+01   -5.030 5.00e-07 ***
    ## workgroup247          -3.513e+01  1.046e+01   -3.359 0.000785 ***
    ## workgroup248          -5.486e+01  2.051e+01   -2.675 0.007483 ** 
    ## workgroup249          -1.074e+02  2.491e+01   -4.312 1.64e-05 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 123.5 on 8409 degrees of freedom
    ## Multiple R-squared:  0.8406, Adjusted R-squared:  0.8397 
    ## F-statistic: 887.1 on 50 and 8409 DF,  p-value: < 2.2e-16

    summary(model2)

    ## 
    ## Call:
    ## lm(formula = processing_time ~ gender * in_degree + gender * 
    ##     out_degree + gender * betweenness + race * in_degree + race * 
    ##     out_degree + race * betweenness + experience + disposal_type + 
    ##     advice_count_final + start_year + workgroup, data = train_data)
    ## 
    ## Residuals:
    ##     Min      1Q  Median      3Q     Max 
    ## -448.27  -80.27   -0.29   81.17  559.57 
    ## 
    ## Coefficients: (2 not defined because of singularities)
    ##                            Estimate Std. Error  t value Pr(>|t|)    
    ## (Intercept)               2.546e+03  1.444e+01  176.371  < 2e-16 ***
    ## gendermale               -2.011e+01  4.375e+00   -4.596 4.37e-06 ***
    ## in_degree                -4.788e-01  2.148e-01   -2.229 0.025861 *  
    ## out_degree               -2.769e-02  7.595e-02   -0.365 0.715464    
    ## betweenness               1.638e-03  3.913e-04    4.184 2.89e-05 ***
    ## raceHispanic              7.405e+01  1.484e+01    4.991 6.12e-07 ***
    ## raceblack                -1.501e+01  1.249e+01   -1.201 0.229645    
    ## raceother                 1.006e+02  4.678e+01    2.150 0.031620 *  
    ## racewhite                -1.249e+01  4.184e+00   -2.986 0.002833 ** 
    ## experience               -7.988e-01  4.506e-03 -177.277  < 2e-16 ***
    ## disposal_typerejected    -1.495e+01  3.645e+00   -4.101 4.16e-05 ***
    ## advice_count_final       -1.885e+00  6.041e-01   -3.121 0.001809 ** 
    ## start_year2001           -3.380e+02  4.479e+00  -75.452  < 2e-16 ***
    ## start_year2002           -6.294e+02  5.487e+00 -114.708  < 2e-16 ***
    ## start_year2003           -9.638e+02  6.521e+00 -147.792  < 2e-16 ***
    ## start_year2004           -1.226e+03  7.596e+00 -161.426  < 2e-16 ***
    ## start_year2005           -1.464e+03  1.011e+01 -144.744  < 2e-16 ***
    ## start_year2006           -1.692e+03  1.675e+01 -101.045  < 2e-16 ***
    ## workgroup162             -1.235e+01  1.668e+01   -0.740 0.459169    
    ## workgroup163              5.634e+01  1.479e+01    3.808 0.000141 ***
    ## workgroup164              1.421e+01  9.717e+00    1.462 0.143762    
    ## workgroup165              9.817e+00  1.231e+01    0.797 0.425348    
    ## workgroup166              6.591e+01  5.522e+01    1.194 0.232646    
    ## workgroup167             -1.835e+01  2.786e+01   -0.659 0.510061    
    ## workgroup171             -1.512e+01  1.502e+01   -1.007 0.313942    
    ## workgroup172             -5.759e+01  1.677e+01   -3.435 0.000595 ***
    ## workgroup173             -4.983e+01  2.116e+01   -2.354 0.018575 *  
    ## workgroup174             -1.731e+01  2.191e+01   -0.790 0.429545    
    ## workgroup175             -1.395e+02  7.109e+01   -1.963 0.049732 *  
    ## workgroup176             -2.185e+01  1.760e+01   -1.241 0.214485    
    ## workgroup177             -2.878e+01  1.826e+01   -1.576 0.114990    
    ## workgroup178             -3.132e+01  1.444e+01   -2.169 0.030130 *  
    ## workgroup179             -3.932e+01  8.124e+00   -4.839 1.33e-06 ***
    ## workgroup211             -5.728e+01  1.049e+01   -5.462 4.85e-08 ***
    ## workgroup212             -7.446e+01  1.111e+01   -6.704 2.16e-11 ***
    ## workgroup213             -8.922e+01  1.497e+01   -5.961 2.61e-09 ***
    ## workgroup214             -6.042e+01  1.575e+01   -3.835 0.000126 ***
    ## workgroup215             -1.171e+02  1.029e+01  -11.383  < 2e-16 ***
    ## workgroup216             -7.827e+01  9.167e+00   -8.538  < 2e-16 ***
    ## workgroup217             -5.313e+01  1.276e+01   -4.165 3.15e-05 ***
    ## workgroup218             -9.075e+01  1.024e+01   -8.861  < 2e-16 ***
    ## workgroup219             -6.383e+01  1.196e+01   -5.337 9.72e-08 ***
    ## workgroup241             -5.790e+01  9.375e+00   -6.176 6.89e-10 ***
    ## workgroup242             -7.396e+01  9.539e+00   -7.754 9.97e-15 ***
    ## workgroup243             -6.345e+01  1.228e+01   -5.168 2.42e-07 ***
    ## workgroup244             -6.928e+01  9.538e+00   -7.263 4.13e-13 ***
    ## workgroup245             -5.130e+01  9.431e+00   -5.439 5.51e-08 ***
    ## workgroup246             -6.372e+01  1.063e+01   -5.994 2.13e-09 ***
    ## workgroup247             -3.961e+01  1.066e+01   -3.716 0.000204 ***
    ## workgroup248             -5.673e+01  2.042e+01   -2.778 0.005481 ** 
    ## workgroup249             -1.137e+02  2.475e+01   -4.594 4.41e-06 ***
    ## gendermale:in_degree     -2.261e-01  2.187e-01   -1.034 0.301160    
    ## gendermale:out_degree     2.357e-01  6.707e-02    3.515 0.000442 ***
    ## gendermale:betweenness    8.211e-04  4.250e-04    1.932 0.053365 .  
    ## in_degree:raceHispanic    1.360e+00  8.437e-01    1.612 0.106899    
    ## in_degree:raceblack      -3.219e+00  9.950e-01   -3.235 0.001221 ** 
    ## in_degree:raceother      -3.875e-01  4.937e+01   -0.008 0.993738    
    ## in_degree:racewhite       1.152e+00  1.631e-01    7.063 1.76e-12 ***
    ## out_degree:raceHispanic  -1.365e+00  2.958e-01   -4.615 3.98e-06 ***
    ## out_degree:raceblack      1.741e+00  2.967e-01    5.869 4.55e-09 ***
    ## out_degree:raceother             NA         NA       NA       NA    
    ## out_degree:racewhite      1.811e-02  7.014e-02    0.258 0.796313    
    ## betweenness:raceHispanic -7.214e-03  1.596e-03   -4.521 6.24e-06 ***
    ## betweenness:raceblack     7.790e-03  2.766e-03    2.816 0.004869 ** 
    ## betweenness:raceother            NA         NA       NA       NA    
    ## betweenness:racewhite    -2.366e-03  3.059e-04   -7.734 1.16e-14 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 122.3 on 8396 degrees of freedom
    ## Multiple R-squared:  0.844,  Adjusted R-squared:  0.8428 
    ## F-statistic: 720.8 on 63 and 8396 DF,  p-value: < 2.2e-16

### effect size

    # Standardizing only continuous variables
    continuous_vars <- c("in_degree", "out_degree", "betweenness", "experience", "advice_count_final")
    train_data[continuous_vars] <- scale(train_data[continuous_vars])

    # Model fitting remains the same
    model2_standardized <- lm(processing_time ~ gender * in_degree + gender * out_degree + gender * betweenness +
      race * in_degree + race * out_degree + race * betweenness +
      experience + disposal_type + advice_count_final + start_year + workgroup,
                              data = train_data)

    summary(model2_standardized)

    ## 
    ## Call:
    ## lm(formula = processing_time ~ gender * in_degree + gender * 
    ##     out_degree + gender * betweenness + race * in_degree + race * 
    ##     out_degree + race * betweenness + experience + disposal_type + 
    ##     advice_count_final + start_year + workgroup, data = train_data)
    ## 
    ## Residuals:
    ##     Min      1Q  Median      3Q     Max 
    ## -448.27  -80.27   -0.29   81.17  559.57 
    ## 
    ## Coefficients: (2 not defined because of singularities)
    ##                            Estimate Std. Error  t value Pr(>|t|)    
    ## (Intercept)                839.9883     8.5451   98.301  < 2e-16 ***
    ## gendermale                  -9.9204     3.1842   -3.116 0.001842 ** 
    ## in_degree                  -10.4658     4.6960   -2.229 0.025861 *  
    ## out_degree                  -1.2607     3.4584   -0.365 0.715464    
    ## betweenness                 20.4905     4.8969    4.184 2.89e-05 ***
    ## raceHispanic                 8.4577     9.5207    0.888 0.374377    
    ## raceblack                   53.4132     9.2937    5.747 9.39e-09 ***
    ## raceother                   97.6182   354.0745    0.276 0.782786    
    ## racewhite                   -9.7603     3.1669   -3.082 0.002063 ** 
    ## experience                -487.3644     2.7492 -177.277  < 2e-16 ***
    ## disposal_typerejected      -14.9471     3.6450   -4.101 4.16e-05 ***
    ## advice_count_final          -4.2865     1.3735   -3.121 0.001809 ** 
    ## start_year2001            -337.9844     4.4795  -75.452  < 2e-16 ***
    ## start_year2002            -629.4220     5.4872 -114.708  < 2e-16 ***
    ## start_year2003            -963.7860     6.5212 -147.792  < 2e-16 ***
    ## start_year2004           -1226.2197     7.5962 -161.426  < 2e-16 ***
    ## start_year2005           -1463.9134    10.1138 -144.744  < 2e-16 ***
    ## start_year2006           -1692.4602    16.7495 -101.045  < 2e-16 ***
    ## workgroup162               -12.3462    16.6784   -0.740 0.459169    
    ## workgroup163                56.3370    14.7940    3.808 0.000141 ***
    ## workgroup164                14.2065     9.7167    1.462 0.143762    
    ## workgroup165                 9.8170    12.3141    0.797 0.425348    
    ## workgroup166                65.9098    55.2168    1.194 0.232646    
    ## workgroup167               -18.3523    27.8584   -0.659 0.510061    
    ## workgroup171               -15.1247    15.0189   -1.007 0.313942    
    ## workgroup172               -57.5923    16.7660   -3.435 0.000595 ***
    ## workgroup173               -49.8282    21.1637   -2.354 0.018575 *  
    ## workgroup174               -17.3094    21.9104   -0.790 0.429545    
    ## workgroup175              -139.5259    71.0945   -1.963 0.049732 *  
    ## workgroup176               -21.8490    17.6000   -1.241 0.214485    
    ## workgroup177               -28.7773    18.2560   -1.576 0.114990    
    ## workgroup178               -31.3223    14.4426   -2.169 0.030130 *  
    ## workgroup179               -39.3154     8.1244   -4.839 1.33e-06 ***
    ## workgroup211               -57.2753    10.4865   -5.462 4.85e-08 ***
    ## workgroup212               -74.4623    11.1071   -6.704 2.16e-11 ***
    ## workgroup213               -89.2191    14.9675   -5.961 2.61e-09 ***
    ## workgroup214               -60.4222    15.7546   -3.835 0.000126 ***
    ## workgroup215              -117.1424    10.2911  -11.383  < 2e-16 ***
    ## workgroup216               -78.2708     9.1672   -8.538  < 2e-16 ***
    ## workgroup217               -53.1312    12.7580   -4.165 3.15e-05 ***
    ## workgroup218               -90.7464    10.2413   -8.861  < 2e-16 ***
    ## workgroup219               -63.8297    11.9607   -5.337 9.72e-08 ***
    ## workgroup241               -57.8977     9.3750   -6.176 6.89e-10 ***
    ## workgroup242               -73.9630     9.5390   -7.754 9.97e-15 ***
    ## workgroup243               -63.4533    12.2778   -5.168 2.42e-07 ***
    ## workgroup244               -69.2761     9.5384   -7.263 4.13e-13 ***
    ## workgroup245               -51.2965     9.4313   -5.439 5.51e-08 ***
    ## workgroup246               -63.7220    10.6309   -5.994 2.13e-09 ***
    ## workgroup247               -39.6086    10.6584   -3.716 0.000204 ***
    ## workgroup248               -56.7252    20.4190   -2.778 0.005481 ** 
    ## workgroup249              -113.6908    24.7468   -4.594 4.41e-06 ***
    ## gendermale:in_degree        -4.9433     4.7807   -1.034 0.301160    
    ## gendermale:out_degree       10.7338     3.0539    3.515 0.000442 ***
    ## gendermale:betweenness      10.2748     5.3176    1.932 0.053365 .  
    ## in_degree:raceHispanic      29.7388    18.4431    1.612 0.106899    
    ## in_degree:raceblack        -70.3620    21.7503   -3.235 0.001221 ** 
    ## in_degree:raceother         -8.4703  1079.2477   -0.008 0.993738    
    ## in_degree:racewhite         25.1773     3.5649    7.063 1.76e-12 ***
    ## out_degree:raceHispanic    -62.1705    13.4700   -4.615 3.98e-06 ***
    ## out_degree:raceblack        79.2956    13.5110    5.869 4.55e-09 ***
    ## out_degree:raceother             NA         NA       NA       NA    
    ## out_degree:racewhite         0.8244     3.1939    0.258 0.796313    
    ## betweenness:raceHispanic   -90.2638    19.9655   -4.521 6.24e-06 ***
    ## betweenness:raceblack       97.4847    34.6142    2.816 0.004869 ** 
    ## betweenness:raceother            NA         NA       NA       NA    
    ## betweenness:racewhite      -29.6056     3.8281   -7.734 1.16e-14 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 122.3 on 8396 degrees of freedom
    ## Multiple R-squared:  0.844,  Adjusted R-squared:  0.8428 
    ## F-statistic: 720.8 on 63 and 8396 DF,  p-value: < 2.2e-16

### Check the multicolinarity

    library(car)

    ## Loading required package: carData

    ## 
    ## Attaching package: 'car'

    ## The following object is masked from 'package:dplyr':
    ## 
    ##     recode

    ## The following object is masked from 'package:purrr':
    ## 
    ##     some

    vif_values <- vif(model)
    print(vif_values)

    ##                        GVIF Df GVIF^(1/(2*Df))
    ## gender             1.109053  1        1.053116
    ## race               1.346833  4        1.037921
    ## experience         4.217506  1        2.053657
    ## in_degree          1.656550  1        1.287070
    ## out_degree         1.256717  1        1.121034
    ## betweenness        1.715243  1        1.309673
    ## disposal_type      1.287079  1        1.134495
    ## advice_count_final 1.063972  1        1.031490
    ## start_year         6.599494  6        1.170287
    ## workgroup          3.568038 33        1.019460

### Check Homoskedasticity and No Auto Correlation

    # Plotting residuals
    residuals <- resid(model)
    fitted_values <- fitted(model)
    plot(fitted_values, residuals, main = "Residuals vs. Fitted", xlab = "Fitted Values", ylab = "Residuals")
    abline(h = 0, col = "red")

![](/Users/kaz/DataspellProjects/org_final/Analysis_files/figure-markdown_strict/unnamed-chunk-17-1.png)

    # Durbin-Watson test
    library(lmtest)
    dwtest(model)

    ## 
    ##  Durbin-Watson test
    ## 
    ## data:  model
    ## DW = 1.9246, p-value = 0.0002372
    ## alternative hypothesis: true autocorrelation is greater than 0

Durbin-Watson test

data: model DW = 1.9397, p-value = 0.0008913 alternative hypothesis:
true autocorrelation is greater than 0

### Normality of Residuals

    qqnorm(residuals, main = "Q-Q Plot of Residuals")
    qqline(residuals, col = "red")

![](/Users/kaz/DataspellProjects/org_final/Analysis_files/figure-markdown_strict/unnamed-chunk-18-1.png)

    predictions <- predict(model, newdata = test_data)
    residuals <- test_data$processing_time - predictions
    RMSE <- sqrt(mean(residuals^2))
    print(paste("RMSE:", RMSE))

    ## [1] "RMSE: 118.91333824876"

### Random Forest

    library(randomForest)

    ## randomForest 4.7-1.1

    ## Type rfNews() to see new features/changes/bug fixes.

    ## 
    ## Attaching package: 'randomForest'

    ## The following object is masked from 'package:dplyr':
    ## 
    ##     combine

    ## The following object is masked from 'package:ggplot2':
    ## 
    ##     margin

    library(caret)

    ## Loading required package: lattice

    ## 
    ## Attaching package: 'caret'

    ## The following object is masked from 'package:purrr':
    ## 
    ##     lift

    # Train a random forest model
    rf_model <- randomForest(processing_time ~  gender + race + experience + in_degree + out_degree + betweenness + disposal_type  + advice_count_final + start_year + workgroup , data = train_data, ntree = 500, mtry = 4, importance = TRUE)

    # Predict using the test data
    predictions <- predict(rf_model, newdata = test_data)

    # Calculate MSE and RMSE
    mse <- mean((predictions - test_data$processing_time)^2)
    rmse <- sqrt(mse)

    print(paste("MSE:", mse))

    ## [1] "MSE: 71839.9218503128"

    print(paste("RMSE:", rmse))

    ## [1] "RMSE: 268.029703298558"

    # Get variable importance
    importance <- importance(rf_model)
    print(importance)

    ##                      %IncMSE IncNodePurity
    ## gender              21.10570       4809874
    ## race                32.68224       6766488
    ## experience         132.86647     375606485
    ## in_degree           31.67287      13669805
    ## out_degree          35.61566      25373614
    ## betweenness         26.22862      19946107
    ## disposal_type       28.27045      11343440
    ## advice_count_final  20.43992       7774249
    ## start_year          90.22770     172133224
    ## workgroup           41.68845     144049450

    # Plot variable importance
    varImpPlot(rf_model)

![](/Users/kaz/DataspellProjects/org_final/Analysis_files/figure-markdown_strict/unnamed-chunk-23-1.png)
