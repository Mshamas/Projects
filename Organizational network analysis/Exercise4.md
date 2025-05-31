## Load the files

You can include R code in the document as follows:

    # change to your own path!
    data_path <- "C:/Users/m_sha/Documents/ONA Assignments/2024-ona-assignments/672_project_data/"
    applications <- read_parquet(paste0(data_path,"app_data_sample.parquet"))
    edges <- read_csv(paste0(data_path,"edges_sample.csv"))

    ## Rows: 32906 Columns: 4
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr  (1): application_number
    ## dbl  (2): ego_examiner_id, alter_examiner_id
    ## date (1): advice_date
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

    applications

    ## # A tibble: 2,018,477 × 16
    ##    application_number filing_date examiner_name_last examiner_name_first
    ##    <chr>              <date>      <chr>              <chr>              
    ##  1 08284457           2000-01-26  HOWARD             JACQUELINE         
    ##  2 08413193           2000-10-11  YILDIRIM           BEKIR              
    ##  3 08531853           2000-05-17  HAMILTON           CYNTHIA            
    ##  4 08637752           2001-07-20  MOSHER             MARY               
    ##  5 08682726           2000-04-10  BARR               MICHAEL            
    ##  6 08687412           2000-04-28  GRAY               LINDA              
    ##  7 08716371           2004-01-26  MCMILLIAN          KARA               
    ##  8 08765941           2000-06-23  FORD               VANESSA            
    ##  9 08776818           2000-02-04  STRZELECKA         TERESA             
    ## 10 08809677           2002-02-20  KIM                SUN                
    ## # ℹ 2,018,467 more rows
    ## # ℹ 12 more variables: examiner_name_middle <chr>, examiner_id <dbl>,
    ## #   examiner_art_unit <dbl>, uspc_class <chr>, uspc_subclass <chr>,
    ## #   patent_number <chr>, patent_issue_date <date>, abandon_date <date>,
    ## #   disposal_type <chr>, appl_status_code <dbl>, appl_status_date <chr>,
    ## #   tc <dbl>

    edges

    ## # A tibble: 32,906 × 4
    ##    application_number advice_date ego_examiner_id alter_examiner_id
    ##    <chr>              <date>                <dbl>             <dbl>
    ##  1 09402488           2008-11-17            84356             66266
    ##  2 09402488           2008-11-17            84356             63519
    ##  3 09402488           2008-11-17            84356             98531
    ##  4 09445135           2008-08-21            92953             71313
    ##  5 09445135           2008-08-21            92953             93865
    ##  6 09445135           2008-08-21            92953             91818
    ##  7 09479304           2008-12-15            61767             69277
    ##  8 09479304           2008-12-15            61767             92446
    ##  9 09479304           2008-12-15            61767             66805
    ## 10 09479304           2008-12-15            61767             70919
    ## # ℹ 32,896 more rows

## Add Gender, Race, Tenure variables for examiners

## Get gender for examiners

    # get a list of first names without repetitions
    examiner_names <- applications %>% 
      distinct(examiner_name_first)

    examiner_names

    ## # A tibble: 2,595 × 1
    ##    examiner_name_first
    ##    <chr>              
    ##  1 JACQUELINE         
    ##  2 BEKIR              
    ##  3 CYNTHIA            
    ##  4 MARY               
    ##  5 MICHAEL            
    ##  6 LINDA              
    ##  7 KARA               
    ##  8 VANESSA            
    ##  9 TERESA             
    ## 10 SUN                
    ## # ℹ 2,585 more rows

    # get a table of names and gender
    examiner_names_gender <- examiner_names %>% 
      do(results = gender(.$examiner_name_first, method = "ssa")) %>% 
      unnest(cols = c(results), keep_empty = TRUE) %>% 
      select(
        examiner_name_first = name,
        gender,
        proportion_female
      )

    examiner_names_gender

    ## # A tibble: 1,822 × 3
    ##    examiner_name_first gender proportion_female
    ##    <chr>               <chr>              <dbl>
    ##  1 AARON               male              0.0082
    ##  2 ABDEL               male              0     
    ##  3 ABDOU               male              0     
    ##  4 ABDUL               male              0     
    ##  5 ABDULHAKIM          male              0     
    ##  6 ABDULLAH            male              0     
    ##  7 ABDULLAHI           male              0     
    ##  8 ABIGAIL             female            0.998 
    ##  9 ABIMBOLA            female            0.944 
    ## 10 ABRAHAM             male              0.0031
    ## # ℹ 1,812 more rows

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

    ##            used  (Mb) gc trigger  (Mb) max used  (Mb)
    ## Ncells  4705773 251.4    8314605 444.1  5130576 274.1
    ## Vcells 49885474 380.6   95873652 731.5 80201246 611.9

    applications

    ## # A tibble: 2,018,477 × 17
    ##    application_number filing_date examiner_name_last examiner_name_first
    ##    <chr>              <date>      <chr>              <chr>              
    ##  1 08284457           2000-01-26  HOWARD             JACQUELINE         
    ##  2 08413193           2000-10-11  YILDIRIM           BEKIR              
    ##  3 08531853           2000-05-17  HAMILTON           CYNTHIA            
    ##  4 08637752           2001-07-20  MOSHER             MARY               
    ##  5 08682726           2000-04-10  BARR               MICHAEL            
    ##  6 08687412           2000-04-28  GRAY               LINDA              
    ##  7 08716371           2004-01-26  MCMILLIAN          KARA               
    ##  8 08765941           2000-06-23  FORD               VANESSA            
    ##  9 08776818           2000-02-04  STRZELECKA         TERESA             
    ## 10 08809677           2002-02-20  KIM                SUN                
    ## # ℹ 2,018,467 more rows
    ## # ℹ 13 more variables: examiner_name_middle <chr>, examiner_id <dbl>,
    ## #   examiner_art_unit <dbl>, uspc_class <chr>, uspc_subclass <chr>,
    ## #   patent_number <chr>, patent_issue_date <date>, abandon_date <date>,
    ## #   disposal_type <chr>, appl_status_code <dbl>, appl_status_date <chr>,
    ## #   tc <dbl>, gender <chr>

## Guess the examiner’s race

    examiner_surnames <- applications %>% 
      select(surname = examiner_name_last) %>% 
      distinct()

    examiner_surnames

    ## # A tibble: 3,806 × 1
    ##    surname   
    ##    <chr>     
    ##  1 HOWARD    
    ##  2 YILDIRIM  
    ##  3 HAMILTON  
    ##  4 MOSHER    
    ##  5 BARR      
    ##  6 GRAY      
    ##  7 MCMILLIAN 
    ##  8 FORD      
    ##  9 STRZELECKA
    ## 10 KIM       
    ## # ℹ 3,796 more rows

    examiner_race <- predict_race(voter.file = examiner_surnames, surname.only = T) %>% 
      as_tibble()

    ## Predicting race for 2020

    ## Warning: Unknown or uninitialised column: `state`.

    ## Proceeding with last name predictions...

    ## ℹ All local files already up-to-date!

    ## 701 (18.4%) individuals' last names were not matched.

    examiner_race

    ## # A tibble: 3,806 × 6
    ##    surname    pred.whi pred.bla pred.his pred.asi pred.oth
    ##    <chr>         <dbl>    <dbl>    <dbl>    <dbl>    <dbl>
    ##  1 HOWARD       0.597   0.295    0.0275   0.00690   0.0741
    ##  2 YILDIRIM     0.807   0.0273   0.0694   0.0165    0.0798
    ##  3 HAMILTON     0.656   0.239    0.0286   0.00750   0.0692
    ##  4 MOSHER       0.915   0.00425  0.0291   0.00917   0.0427
    ##  5 BARR         0.784   0.120    0.0268   0.00830   0.0615
    ##  6 GRAY         0.640   0.252    0.0281   0.00748   0.0724
    ##  7 MCMILLIAN    0.322   0.554    0.0212   0.00340   0.0995
    ##  8 FORD         0.576   0.320    0.0275   0.00621   0.0697
    ##  9 STRZELECKA   0.472   0.171    0.220    0.0825    0.0543
    ## 10 KIM          0.0169  0.00282  0.00546  0.943     0.0319
    ## # ℹ 3,796 more rows

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

    examiner_race

    ## # A tibble: 3,806 × 8
    ##    surname    pred.whi pred.bla pred.his pred.asi pred.oth max_race_p race 
    ##    <chr>         <dbl>    <dbl>    <dbl>    <dbl>    <dbl>      <dbl> <chr>
    ##  1 HOWARD       0.597   0.295    0.0275   0.00690   0.0741      0.597 white
    ##  2 YILDIRIM     0.807   0.0273   0.0694   0.0165    0.0798      0.807 white
    ##  3 HAMILTON     0.656   0.239    0.0286   0.00750   0.0692      0.656 white
    ##  4 MOSHER       0.915   0.00425  0.0291   0.00917   0.0427      0.915 white
    ##  5 BARR         0.784   0.120    0.0268   0.00830   0.0615      0.784 white
    ##  6 GRAY         0.640   0.252    0.0281   0.00748   0.0724      0.640 white
    ##  7 MCMILLIAN    0.322   0.554    0.0212   0.00340   0.0995      0.554 black
    ##  8 FORD         0.576   0.320    0.0275   0.00621   0.0697      0.576 white
    ##  9 STRZELECKA   0.472   0.171    0.220    0.0825    0.0543      0.472 white
    ## 10 KIM          0.0169  0.00282  0.00546  0.943     0.0319      0.943 Asian
    ## # ℹ 3,796 more rows

    # removing extra columns
    examiner_race <- examiner_race %>% 
      select(surname,race)

    applications <- applications %>% 
      left_join(examiner_race, by = c("examiner_name_last" = "surname"))

    rm(examiner_race)
    rm(examiner_surnames)
    gc()

    ##            used  (Mb) gc trigger  (Mb) max used  (Mb)
    ## Ncells  4797186 256.2    8314605 444.1  6845160 365.6
    ## Vcells 52072563 397.3   95873652 731.5 95599430 729.4

    applications

    ## # A tibble: 2,018,477 × 18
    ##    application_number filing_date examiner_name_last examiner_name_first
    ##    <chr>              <date>      <chr>              <chr>              
    ##  1 08284457           2000-01-26  HOWARD             JACQUELINE         
    ##  2 08413193           2000-10-11  YILDIRIM           BEKIR              
    ##  3 08531853           2000-05-17  HAMILTON           CYNTHIA            
    ##  4 08637752           2001-07-20  MOSHER             MARY               
    ##  5 08682726           2000-04-10  BARR               MICHAEL            
    ##  6 08687412           2000-04-28  GRAY               LINDA              
    ##  7 08716371           2004-01-26  MCMILLIAN          KARA               
    ##  8 08765941           2000-06-23  FORD               VANESSA            
    ##  9 08776818           2000-02-04  STRZELECKA         TERESA             
    ## 10 08809677           2002-02-20  KIM                SUN                
    ## # ℹ 2,018,467 more rows
    ## # ℹ 14 more variables: examiner_name_middle <chr>, examiner_id <dbl>,
    ## #   examiner_art_unit <dbl>, uspc_class <chr>, uspc_subclass <chr>,
    ## #   patent_number <chr>, patent_issue_date <date>, abandon_date <date>,
    ## #   disposal_type <chr>, appl_status_code <dbl>, appl_status_date <chr>,
    ## #   tc <dbl>, gender <chr>, race <chr>

## Examiner’s tenure

    examiner_dates <- applications %>% 
      select(examiner_id, filing_date, appl_status_date) 

    examiner_dates

    ## # A tibble: 2,018,477 × 3
    ##    examiner_id filing_date appl_status_date  
    ##          <dbl> <date>      <chr>             
    ##  1       96082 2000-01-26  30jan2003 00:00:00
    ##  2       87678 2000-10-11  27sep2010 00:00:00
    ##  3       63213 2000-05-17  30mar2009 00:00:00
    ##  4       73788 2001-07-20  07sep2009 00:00:00
    ##  5       77294 2000-04-10  19apr2001 00:00:00
    ##  6       68606 2000-04-28  16jul2001 00:00:00
    ##  7       89557 2004-01-26  15may2017 00:00:00
    ##  8       97543 2000-06-23  03apr2002 00:00:00
    ##  9       98714 2000-02-04  27nov2002 00:00:00
    ## 10       65530 2002-02-20  23mar2009 00:00:00
    ## # ℹ 2,018,467 more rows

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

    examiner_dates

    ## # A tibble: 5,625 × 4
    ##    examiner_id earliest_date latest_date tenure_days
    ##          <dbl> <date>        <date>            <dbl>
    ##  1       59012 2004-07-28    2015-07-24         4013
    ##  2       59025 2009-10-26    2017-05-18         2761
    ##  3       59030 2005-12-12    2017-05-22         4179
    ##  4       59040 2007-09-11    2017-05-23         3542
    ##  5       59052 2001-08-21    2007-02-28         2017
    ##  6       59054 2000-11-10    2016-12-23         5887
    ##  7       59055 2004-11-02    2007-12-26         1149
    ##  8       59056 2000-03-24    2017-05-22         6268
    ##  9       59074 2000-01-31    2017-03-17         6255
    ## 10       59081 2011-04-21    2017-05-19         2220
    ## # ℹ 5,615 more rows

    applications <- applications %>% 
      left_join(examiner_dates, by = "examiner_id")

    rm(examiner_dates)
    gc()

    ##            used  (Mb) gc trigger   (Mb)  max used   (Mb)
    ## Ncells  4803642 256.6   15094424  806.2  15094424  806.2
    ## Vcells 64434408 491.6  138234058 1054.7 138087308 1053.6

    applications

    ## # A tibble: 2,018,477 × 21
    ##    application_number filing_date examiner_name_last examiner_name_first
    ##    <chr>              <date>      <chr>              <chr>              
    ##  1 08284457           2000-01-26  HOWARD             JACQUELINE         
    ##  2 08413193           2000-10-11  YILDIRIM           BEKIR              
    ##  3 08531853           2000-05-17  HAMILTON           CYNTHIA            
    ##  4 08637752           2001-07-20  MOSHER             MARY               
    ##  5 08682726           2000-04-10  BARR               MICHAEL            
    ##  6 08687412           2000-04-28  GRAY               LINDA              
    ##  7 08716371           2004-01-26  MCMILLIAN          KARA               
    ##  8 08765941           2000-06-23  FORD               VANESSA            
    ##  9 08776818           2000-02-04  STRZELECKA         TERESA             
    ## 10 08809677           2002-02-20  KIM                SUN                
    ## # ℹ 2,018,467 more rows
    ## # ℹ 17 more variables: examiner_name_middle <chr>, examiner_id <dbl>,
    ## #   examiner_art_unit <dbl>, uspc_class <chr>, uspc_subclass <chr>,
    ## #   patent_number <chr>, patent_issue_date <date>, abandon_date <date>,
    ## #   disposal_type <chr>, appl_status_code <dbl>, appl_status_date <chr>,
    ## #   tc <dbl>, gender <chr>, race <chr>, earliest_date <date>,
    ## #   latest_date <date>, tenure_days <dbl>

## Pick two workgroups you want to focus on (remember that a workgroup is

## represented by the first 3 digits of `examiner_art_unit` value)

How do they compare on examiners’ demographics? Show summary statistics
and plots.

    group_172 = applications[substr(applications$examiner_art_unit, 1,3)==172,]
    group_175 = applications[substr(applications$examiner_art_unit, 1,3)==175,]
    summary(group_172)

    ##  application_number  filing_date         examiner_name_last examiner_name_first
    ##  Length:79195       Min.   :2000-01-03   Length:79195       Length:79195       
    ##  Class :character   1st Qu.:2004-01-20   Class :character   Class :character   
    ##  Mode  :character   Median :2009-07-17   Mode  :character   Mode  :character   
    ##                     Mean   :2008-12-01                                         
    ##                     3rd Qu.:2013-05-20                                         
    ##                     Max.   :2017-05-01                                         
    ##                                                                                
    ##  examiner_name_middle  examiner_id    examiner_art_unit  uspc_class       
    ##  Length:79195         Min.   :59040   Min.   :1721      Length:79195      
    ##  Class :character     1st Qu.:65638   1st Qu.:1722      Class :character  
    ##  Mode  :character     Median :74727   Median :1724      Mode  :character  
    ##                       Mean   :77666   Mean   :1724                        
    ##                       3rd Qu.:91210   3rd Qu.:1726                        
    ##                       Max.   :99316   Max.   :1729                        
    ##                       NA's   :145                                         
    ##  uspc_subclass      patent_number      patent_issue_date   
    ##  Length:79195       Length:79195       Min.   :2000-10-10  
    ##  Class :character   Class :character   1st Qu.:2005-04-26  
    ##  Mode  :character   Mode  :character   Median :2011-10-25  
    ##                                        Mean   :2010-03-25  
    ##                                        3rd Qu.:2014-09-30  
    ##                                        Max.   :2017-06-20  
    ##                                        NA's   :32455       
    ##   abandon_date        disposal_type      appl_status_code appl_status_date  
    ##  Min.   :2000-08-18   Length:79195       Min.   :  1.0    Length:79195      
    ##  1st Qu.:2007-06-21   Class :character   1st Qu.:150.0    Class :character  
    ##  Median :2012-03-30   Mode  :character   Median :150.0    Mode  :character  
    ##  Mean   :2011-06-01                      Mean   :149.6                      
    ##  3rd Qu.:2014-08-15                      3rd Qu.:161.0                      
    ##  Max.   :2017-06-01                      Max.   :454.0                      
    ##  NA's   :59648                           NA's   :165                        
    ##        tc          gender              race           earliest_date       
    ##  Min.   :1700   Length:79195       Length:79195       Min.   :2000-01-03  
    ##  1st Qu.:1700   Class :character   Class :character   1st Qu.:2000-01-06  
    ##  Median :1700   Mode  :character   Mode  :character   Median :2000-01-19  
    ##  Mean   :1700                                         Mean   :2002-02-27  
    ##  3rd Qu.:1700                                         3rd Qu.:2004-03-17  
    ##  Max.   :1700                                         Max.   :2014-01-10  
    ##                                                       NA's   :145         
    ##   latest_date          tenure_days  
    ##  Min.   :2005-01-10   Min.   : 435  
    ##  1st Qu.:2017-05-19   1st Qu.:4800  
    ##  Median :2017-05-22   Median :6314  
    ##  Mean   :2017-05-12   Mean   :5553  
    ##  3rd Qu.:2017-05-23   3rd Qu.:6342  
    ##  Max.   :2017-05-23   Max.   :6350  
    ##  NA's   :145          NA's   :145

    summary(group_175)

    ##  application_number  filing_date         examiner_name_last examiner_name_first
    ##  Length:58207       Min.   :2000-01-03   Length:58207       Length:58207       
    ##  Class :character   1st Qu.:2002-03-05   Class :character   Class :character   
    ##  Mode  :character   Median :2004-06-14   Mode  :character   Mode  :character   
    ##                     Mean   :2006-10-28                                         
    ##                     3rd Qu.:2012-01-10                                         
    ##                     Max.   :2017-04-29                                         
    ##                                                                                
    ##  examiner_name_middle  examiner_id    examiner_art_unit  uspc_class       
    ##  Length:58207         Min.   :59227   Min.   :1751      Length:58207      
    ##  Class :character     1st Qu.:66092   1st Qu.:1753      Class :character  
    ##  Mode  :character     Median :75641   Median :1755      Mode  :character  
    ##                       Mean   :79826   Mean   :1755                        
    ##                       3rd Qu.:95160   3rd Qu.:1756                        
    ##                       Max.   :99879   Max.   :1759                        
    ##                       NA's   :303                                         
    ##  uspc_subclass      patent_number      patent_issue_date   
    ##  Length:58207       Length:58207       Min.   :1997-03-04  
    ##  Class :character   Class :character   1st Qu.:2003-11-11  
    ##  Mode  :character   Mode  :character   Median :2005-09-20  
    ##                                        Mean   :2007-03-23  
    ##                                        3rd Qu.:2008-01-01  
    ##                                        Max.   :2017-06-20  
    ##                                        NA's   :24040       
    ##   abandon_date        disposal_type      appl_status_code appl_status_date  
    ##  Min.   :2000-05-04   Length:58207       Min.   : 17.0    Length:58207      
    ##  1st Qu.:2005-08-24   Class :character   1st Qu.:150.0    Class :character  
    ##  Median :2012-09-11   Mode  :character   Median :150.0    Mode  :character  
    ##  Mean   :2010-05-09                      Mean   :161.4                      
    ##  3rd Qu.:2014-10-17                      3rd Qu.:161.0                      
    ##  Max.   :2017-06-01                      Max.   :454.0                      
    ##  NA's   :41948                           NA's   :60                         
    ##        tc          gender              race           earliest_date       
    ##  Min.   :1700   Length:58207       Length:58207       Min.   :2000-01-03  
    ##  1st Qu.:1700   Class :character   Class :character   1st Qu.:2000-01-05  
    ##  Median :1700   Mode  :character   Mode  :character   Median :2000-01-10  
    ##  Mean   :1700                                         Mean   :2002-02-18  
    ##  3rd Qu.:1700                                         3rd Qu.:2004-02-19  
    ##  Max.   :1700                                         Max.   :2014-05-23  
    ##                                                       NA's   :891         
    ##   latest_date          tenure_days  
    ##  Min.   :2000-12-27   Min.   : 267  
    ##  1st Qu.:2017-05-19   1st Qu.:4842  
    ##  Median :2017-05-20   Median :6330  
    ##  Mean   :2017-05-05   Mean   :5555  
    ##  3rd Qu.:2017-05-23   3rd Qu.:6346  
    ##  Max.   :2017-07-24   Max.   :6391  
    ##  NA's   :891          NA's   :891

\##Create network graph

    # get examiner ids to use as nodes
    examiner_ids = distinct(subset(applications, select=c(examiner_art_unit, examiner_id)))
    examiner_ids$workgroup = substr(examiner_ids$examiner_art_unit, 1,3)
    examiner_ids = examiner_ids[examiner_ids$workgroup==172 | examiner_ids$workgroup==175,]

    # merge with edges dataframe to get final edge table
    data.f = merge(x=edges, y=examiner_ids, by.x="ego_examiner_id", by.y="examiner_id", all.x=TRUE)
    data.f = data.f %>% rename(ego_art_unit=examiner_art_unit, ego_workgroup=workgroup)
    data.f = drop_na(data.f)

    data.f = merge(x=data.f, y=examiner_ids, by.x="alter_examiner_id", by.y="examiner_id", all.x=TRUE)
    data.f = data.f %>% rename(alter_art_unit=examiner_art_unit, alter_workgroup=workgroup)
    data.f = drop_na(data.f)

    # get unique ego and alter nodes
    ego_nodes = subset(data.f, select=c(ego_examiner_id,ego_art_unit, ego_workgroup)) %>% rename(examiner_id=ego_examiner_id,art_unit=ego_art_unit,workgroup=ego_workgroup)
    alter_nodes = subset(data.f, select=c(alter_examiner_id,alter_art_unit, alter_workgroup))%>% rename(examiner_id=alter_examiner_id,art_unit=alter_art_unit,workgroup=alter_workgroup)
    nodes = rbind(ego_nodes, alter_nodes)
    nodes = distinct(nodes)
    nodes = nodes %>% group_by(examiner_id) %>% summarise(examiner_id=first(examiner_id), art_unit=first(art_unit), workgroup=first(workgroup))

    # creating network
    advice_net = graph_from_data_frame(d=data.f, vertices=nodes, directed=TRUE)

### Create variable for application processing time ‘app\_proc\_time’ that measures the number of days (or weeks) from application filing date, until the final decision on it (patented or abandoned)

    # filter for examiner ids to consider (nodes)
    applications_2 <- applications %>%
          filter(examiner_id %in% nodes$examiner_id)

    # Convert to class date
    applications_2 <- applications_2 %>% 
      mutate(patent_issue_date = as.Date(patent_issue_date, format = "%YYYY-%mm-%dd"))
    applications_2 <- applications_2 %>% 
      mutate(abandon_date = as.Date(abandon_date, format = "%YYYY-%mm-%dd"))

    app_proc_time <- c()
    for (i in 1:nrow(applications_2)){
      # if patent issue date is NA, use abandon date
      if (is.na(applications[i,11])){
        #app_proc_time[i] = interval(applications_2[i,2] ,applications_2[i,11] )
        app_proc_time[i] = applications_2[i,12] - applications_2[i,2]
      }
      else{
        #app_proc_time[i] = interval(applications_2[i,2] ,applications_2[i,12] )
        app_proc_time[i] = applications_2[i,11] - applications_2[i,2]
      }
      
    }

    applications_2$app_proc_time = app_proc_time

### Join with nodes dataset: add gender, race, app\_proc\_time, tenure and other relevant variables

    # remove columns not needed for regression from the applications table
    applications_2 <- applications_2 %>% 
      select(examiner_id, gender, race, app_proc_time,tenure_days)
    # remove NaN values
    applications_2<- na.omit(applications_2)
    applications_2 <- subset(applications_2,!duplicated(applications_2$examiner_id))
    # joining gender back to the dataset
    nodes <- nodes %>% 
      left_join(applications_2, by = "examiner_id")

### add centrality values as columns in nodes dataframe

    Degree <- degree(advice_net, v=V(advice_net))
    nodes$Degree <- Degree
    Betweenness <- betweenness(advice_net)
    nodes$Betweenness <- Betweenness
    Closeness <- closeness(advice_net)
    nodes$Closeness <- Closeness

### Use linear regression models `lm()` to estimate the relationship between centrality and `app_proc_time`, Does this relationship differ by examiner gender? Include Interaction term

    library('stargazer')

    ## 
    ## Please cite as:

    ##  Hlavac, Marek (2022). stargazer: Well-Formatted Regression and Summary Statistics Tables.

    ##  R package version 5.2.3. https://CRAN.R-project.org/package=stargazer

    # Assuming other variables has 147 observations and you want to match this number
    app_proc_time = na.omit(unlist(app_proc_time))
    app_proc_time_subset = unlist(app_proc_time)[1:length(Degree)]

    # create linear regression
    lr <- lm(app_proc_time_subset ~ Degree + Closeness + Betweenness +
               tenure_days+ art_unit + workgroup+ race, nodes)

    # view model summary
    summary(lr)

    ## 
    ## Call:
    ## lm(formula = app_proc_time_subset ~ Degree + Closeness + Betweenness + 
    ##     tenure_days + art_unit + workgroup + race, data = nodes)
    ## 
    ## Residuals:
    ##     Min      1Q  Median      3Q     Max 
    ## -637.76 -242.73  -66.87  187.89 1318.33 
    ## 
    ## Coefficients:
    ##                Estimate Std. Error t value Pr(>|t|)
    ## (Intercept)   5.267e+04  4.376e+04   1.204    0.233
    ## Degree       -2.252e-01  6.047e-01  -0.372    0.711
    ## Closeness    -1.369e+02  1.307e+02  -1.047    0.299
    ## Betweenness  -1.985e+00  3.586e+00  -0.554    0.582
    ## tenure_days   5.478e-02  1.512e-01   0.362    0.718
    ## art_unit     -3.023e+01  2.539e+01  -1.191    0.238
    ## workgroup175  8.961e+02  7.769e+02   1.153    0.253
    ## raceblack     1.080e+02  2.875e+02   0.376    0.708
    ## raceHispanic -4.486e+01  4.518e+02  -0.099    0.921
    ## racewhite     5.647e+01  1.601e+02   0.353    0.725
    ## 
    ## Residual standard error: 407.2 on 68 degrees of freedom
    ##   (69 observations deleted due to missingness)
    ## Multiple R-squared:  0.05108,    Adjusted R-squared:  -0.07451 
    ## F-statistic: 0.4067 on 9 and 68 DF,  p-value: 0.9274

    stargazer(lr, type="html")

    ## 
    ## <table style="text-align:center"><tr><td colspan="2" style="border-bottom: 1px solid black"></td></tr><tr><td style="text-align:left"></td><td><em>Dependent variable:</em></td></tr>
    ## <tr><td></td><td colspan="1" style="border-bottom: 1px solid black"></td></tr>
    ## <tr><td style="text-align:left"></td><td>app_proc_time_subset</td></tr>
    ## <tr><td colspan="2" style="border-bottom: 1px solid black"></td></tr><tr><td style="text-align:left">Degree</td><td>-0.225</td></tr>
    ## <tr><td style="text-align:left"></td><td>(0.605)</td></tr>
    ## <tr><td style="text-align:left"></td><td></td></tr>
    ## <tr><td style="text-align:left">Closeness</td><td>-136.904</td></tr>
    ## <tr><td style="text-align:left"></td><td>(130.736)</td></tr>
    ## <tr><td style="text-align:left"></td><td></td></tr>
    ## <tr><td style="text-align:left">Betweenness</td><td>-1.985</td></tr>
    ## <tr><td style="text-align:left"></td><td>(3.586)</td></tr>
    ## <tr><td style="text-align:left"></td><td></td></tr>
    ## <tr><td style="text-align:left">tenure_days</td><td>0.055</td></tr>
    ## <tr><td style="text-align:left"></td><td>(0.151)</td></tr>
    ## <tr><td style="text-align:left"></td><td></td></tr>
    ## <tr><td style="text-align:left">art_unit</td><td>-30.234</td></tr>
    ## <tr><td style="text-align:left"></td><td>(25.385)</td></tr>
    ## <tr><td style="text-align:left"></td><td></td></tr>
    ## <tr><td style="text-align:left">workgroup175</td><td>896.083</td></tr>
    ## <tr><td style="text-align:left"></td><td>(776.873)</td></tr>
    ## <tr><td style="text-align:left"></td><td></td></tr>
    ## <tr><td style="text-align:left">raceblack</td><td>108.050</td></tr>
    ## <tr><td style="text-align:left"></td><td>(287.462)</td></tr>
    ## <tr><td style="text-align:left"></td><td></td></tr>
    ## <tr><td style="text-align:left">raceHispanic</td><td>-44.865</td></tr>
    ## <tr><td style="text-align:left"></td><td>(451.764)</td></tr>
    ## <tr><td style="text-align:left"></td><td></td></tr>
    ## <tr><td style="text-align:left">racewhite</td><td>56.467</td></tr>
    ## <tr><td style="text-align:left"></td><td>(160.079)</td></tr>
    ## <tr><td style="text-align:left"></td><td></td></tr>
    ## <tr><td style="text-align:left">Constant</td><td>52,671.660</td></tr>
    ## <tr><td style="text-align:left"></td><td>(43,757.400)</td></tr>
    ## <tr><td style="text-align:left"></td><td></td></tr>
    ## <tr><td colspan="2" style="border-bottom: 1px solid black"></td></tr><tr><td style="text-align:left">Observations</td><td>78</td></tr>
    ## <tr><td style="text-align:left">R<sup>2</sup></td><td>0.051</td></tr>
    ## <tr><td style="text-align:left">Adjusted R<sup>2</sup></td><td>-0.075</td></tr>
    ## <tr><td style="text-align:left">Residual Std. Error</td><td>407.248 (df = 68)</td></tr>
    ## <tr><td style="text-align:left">F Statistic</td><td>0.407 (df = 9; 68)</td></tr>
    ## <tr><td colspan="2" style="border-bottom: 1px solid black"></td></tr><tr><td style="text-align:left"><em>Note:</em></td><td style="text-align:right"><sup>*</sup>p<0.1; <sup>**</sup>p<0.05; <sup>***</sup>p<0.01</td></tr>
    ## </table>

    library(ggplot2)

    # Coefficients to data frame
    coef_df <- data.frame(
      Term = names(coef(lr)),
      Estimate = coef(lr),
      Std.Error = summary(lr)$coefficients[, "Std. Error"]
    )

    # Plot
    ggplot(coef_df, aes(x = Term, y = Estimate, fill = Term)) +
      geom_col() +
      geom_errorbar(aes(ymin = Estimate - Std.Error, ymax = Estimate + Std.Error), width = 0.2) +
      theme_minimal() +
      theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
      labs(y = "Coefficient Estimate", title = "Regression Coefficients")

![](Exercise4_files/figure-markdown_strict/unnamed-chunk-24-1.png)

    # create linear regression
    lr2 <- lm(app_proc_time_subset ~ Degree +Closeness + Betweenness +
               tenure_days + art_unit + workgroup + Degree*gender + Betweenness*gender + race + Closeness*gender , nodes)
    # view model summary
    summary(lr2)

    ## 
    ## Call:
    ## lm(formula = app_proc_time_subset ~ Degree + Closeness + Betweenness + 
    ##     tenure_days + art_unit + workgroup + Degree * gender + Betweenness * 
    ##     gender + race + Closeness * gender, data = nodes)
    ## 
    ## Residuals:
    ##     Min      1Q  Median      3Q     Max 
    ## -611.06 -285.04  -57.87  178.33 1276.14 
    ## 
    ## Coefficients:
    ##                          Estimate Std. Error t value Pr(>|t|)
    ## (Intercept)             3.948e+04  4.820e+04   0.819    0.416
    ## Degree                 -1.262e+00  1.781e+00  -0.709    0.481
    ## Closeness              -4.374e+02  3.637e+02  -1.203    0.233
    ## Betweenness            -2.618e+01  2.037e+01  -1.285    0.203
    ## tenure_days             2.831e-02  1.604e-01   0.177    0.860
    ## art_unit               -2.229e+01  2.796e+01  -0.797    0.428
    ## workgroup175            6.729e+02  8.511e+02   0.791    0.432
    ## gendermale             -2.490e+02  2.865e+02  -0.869    0.388
    ## raceblack               1.399e+01  3.366e+02   0.042    0.967
    ## raceHispanic           -1.660e+02  4.637e+02  -0.358    0.722
    ## racewhite              -6.838e+01  1.826e+02  -0.375    0.709
    ## Degree:gendermale       1.204e+00  1.878e+00   0.641    0.524
    ## Betweenness:gendermale  2.514e+01  2.072e+01   1.213    0.230
    ## Closeness:gendermale    3.349e+02  3.988e+02   0.840    0.404
    ## 
    ## Residual standard error: 411.5 on 64 degrees of freedom
    ##   (69 observations deleted due to missingness)
    ## Multiple R-squared:  0.08805,    Adjusted R-squared:  -0.09719 
    ## F-statistic: 0.4753 on 13 and 64 DF,  p-value: 0.9307

    stargazer(lr2, type="html")

    ## 
    ## <table style="text-align:center"><tr><td colspan="2" style="border-bottom: 1px solid black"></td></tr><tr><td style="text-align:left"></td><td><em>Dependent variable:</em></td></tr>
    ## <tr><td></td><td colspan="1" style="border-bottom: 1px solid black"></td></tr>
    ## <tr><td style="text-align:left"></td><td>app_proc_time_subset</td></tr>
    ## <tr><td colspan="2" style="border-bottom: 1px solid black"></td></tr><tr><td style="text-align:left">Degree</td><td>-1.262</td></tr>
    ## <tr><td style="text-align:left"></td><td>(1.781)</td></tr>
    ## <tr><td style="text-align:left"></td><td></td></tr>
    ## <tr><td style="text-align:left">Closeness</td><td>-437.439</td></tr>
    ## <tr><td style="text-align:left"></td><td>(363.679)</td></tr>
    ## <tr><td style="text-align:left"></td><td></td></tr>
    ## <tr><td style="text-align:left">Betweenness</td><td>-26.180</td></tr>
    ## <tr><td style="text-align:left"></td><td>(20.372)</td></tr>
    ## <tr><td style="text-align:left"></td><td></td></tr>
    ## <tr><td style="text-align:left">tenure_days</td><td>0.028</td></tr>
    ## <tr><td style="text-align:left"></td><td>(0.160)</td></tr>
    ## <tr><td style="text-align:left"></td><td></td></tr>
    ## <tr><td style="text-align:left">art_unit</td><td>-22.291</td></tr>
    ## <tr><td style="text-align:left"></td><td>(27.962)</td></tr>
    ## <tr><td style="text-align:left"></td><td></td></tr>
    ## <tr><td style="text-align:left">workgroup175</td><td>672.894</td></tr>
    ## <tr><td style="text-align:left"></td><td>(851.078)</td></tr>
    ## <tr><td style="text-align:left"></td><td></td></tr>
    ## <tr><td style="text-align:left">gendermale</td><td>-249.019</td></tr>
    ## <tr><td style="text-align:left"></td><td>(286.477)</td></tr>
    ## <tr><td style="text-align:left"></td><td></td></tr>
    ## <tr><td style="text-align:left">raceblack</td><td>13.991</td></tr>
    ## <tr><td style="text-align:left"></td><td>(336.619)</td></tr>
    ## <tr><td style="text-align:left"></td><td></td></tr>
    ## <tr><td style="text-align:left">raceHispanic</td><td>-165.975</td></tr>
    ## <tr><td style="text-align:left"></td><td>(463.670)</td></tr>
    ## <tr><td style="text-align:left"></td><td></td></tr>
    ## <tr><td style="text-align:left">racewhite</td><td>-68.383</td></tr>
    ## <tr><td style="text-align:left"></td><td>(182.569)</td></tr>
    ## <tr><td style="text-align:left"></td><td></td></tr>
    ## <tr><td style="text-align:left">Degree:gendermale</td><td>1.204</td></tr>
    ## <tr><td style="text-align:left"></td><td>(1.878)</td></tr>
    ## <tr><td style="text-align:left"></td><td></td></tr>
    ## <tr><td style="text-align:left">Betweenness:gendermale</td><td>25.139</td></tr>
    ## <tr><td style="text-align:left"></td><td>(20.724)</td></tr>
    ## <tr><td style="text-align:left"></td><td></td></tr>
    ## <tr><td style="text-align:left">Closeness:gendermale</td><td>334.946</td></tr>
    ## <tr><td style="text-align:left"></td><td>(398.774)</td></tr>
    ## <tr><td style="text-align:left"></td><td></td></tr>
    ## <tr><td style="text-align:left">Constant</td><td>39,480.940</td></tr>
    ## <tr><td style="text-align:left"></td><td>(48,195.620)</td></tr>
    ## <tr><td style="text-align:left"></td><td></td></tr>
    ## <tr><td colspan="2" style="border-bottom: 1px solid black"></td></tr><tr><td style="text-align:left">Observations</td><td>78</td></tr>
    ## <tr><td style="text-align:left">R<sup>2</sup></td><td>0.088</td></tr>
    ## <tr><td style="text-align:left">Adjusted R<sup>2</sup></td><td>-0.097</td></tr>
    ## <tr><td style="text-align:left">Residual Std. Error</td><td>411.524 (df = 64)</td></tr>
    ## <tr><td style="text-align:left">F Statistic</td><td>0.475 (df = 13; 64)</td></tr>
    ## <tr><td colspan="2" style="border-bottom: 1px solid black"></td></tr><tr><td style="text-align:left"><em>Note:</em></td><td style="text-align:right"><sup>*</sup>p<0.1; <sup>**</sup>p<0.05; <sup>***</sup>p<0.01</td></tr>
    ## </table>

    # Coefficients to data frame
    coef_df <- data.frame(
      Term = names(coef(lr2)),
      Estimate = coef(lr2),
      Std.Error = summary(lr2)$coefficients[, "Std. Error"]
    )

    # Plot
    ggplot(coef_df, aes(x = Term, y = Estimate, fill = Term)) +
      geom_col() +
      geom_errorbar(aes(ymin = Estimate - Std.Error, ymax = Estimate + Std.Error), width = 0.2) +
      theme_minimal() +
      theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
      labs(y = "Coefficient Estimate", title = "Regression Coefficients")

![](Exercise4_files/figure-markdown_strict/unnamed-chunk-26-1.png)

Based on your linear regression analysis exploring the relationship
between examiner centrality (measured through metrics such as Degree,
Closeness, and Betweenness) and patent application processing times
(`app_proc_time`), while controlling for other examiner characteristics
(tenure, art unit, workgroup, race, and gender), here’s a discussion of
the findings and their implications for the USPTO:

### Understanding the Relationship Between Centrality and Processing Time

The models aimed to quantify how an examiner’s position within their
professional network (centrality) might impact the efficiency
(processing time) of patent examination. Centrality metrics, such as
Degree, Closeness, and Betweenness, serve as proxies for the examiner’s
connectedness, accessibility, and control over the flow of information
within the network, respectively.

### Controlling for Examiner Characteristics

By including variables such as tenure days, art unit, workgroup, and
demographic characteristics (race and gender), the models accounted for
a broad spectrum of factors that could influence processing times. These
controls are crucial for isolating the effect of centrality from other
influences that might confound the relationship under investigation.

### Impact of Gender on the Centrality-Processing Time Relationship

The incorporation of interaction terms between centrality measures and
gender (e.g., `Degree * gender`, `Betweenness * gender`) was intended to
explore whether the centrality’s impact on processing times varies by
gender. This approach helps in understanding not just the direct effect
of centrality on processing times but also how this effect might differ
across genders, potentially shedding light on nuances in the work
dynamics at the USPTO.

### Key Findings and Interpretations

1.  **Limited Direct Impact of Centrality**: The regression models did
    not reveal statistically significant coefficients for centrality
    measures, suggesting that, within the scope of the analyzed data,
    centrality alone does not have a direct, measurable impact on
    processing times. This could imply that the efficiency of patent
    processing at the USPTO might not be heavily dependent on network
    position, or that the linear model’s specification may not capture
    the complexities of this relationship.

2.  **No Clear Gender Moderation**: The lack of significance in the
    interaction terms suggests that the relationship between centrality
    and processing times does not significantly differ by examiner
    gender. This finding implies that, at least in terms of network
    centrality, there might not be substantial gender-based disparities
    in how network position influences processing efficiency.

3.  **Overall Model Significance and Fit**: Given the models’ low
    R-squared values and non-significant F-statistics, it appears that
    centrality and the selected examiner characteristics do not
    comprehensively explain the variance in processing times. This
    outcome suggests the presence of other influential factors not
    captured by the model or the need for alternative modeling
    approaches.

### Implications for the USPTO

-   **Policy and Training**: The findings suggest that initiatives aimed
    at enhancing processing efficiency might not need to focus heavily
    on altering network structures or centrality. Instead, focusing on
    other aspects, such as resource allocation, examiner training, or
    workflow optimization, might be more beneficial.
-   **Equity and Inclusion**: The absence of significant gender
    differences in how centrality affects processing times could be seen
    as a positive indication of gender equity in terms of network
    influence. However, the USPTO may still benefit from continued
    efforts to ensure an inclusive work environment that supports all
    examiners equally, irrespective of their network position.
-   **Further Research**: These results highlight the need for further
    investigation into what drives efficiency in patent processing.
    Qualitative studies or alternative quantitative approaches, such as
    machine learning models that can capture non-linear effects and
    interactions, might offer deeper insights.

In conclusion, while the analysis did not demonstrate a significant
direct impact of examiner centrality on patent application processing
times or substantial differences by gender, it underscores the
complexity of the examination process and the potential for other
factors to play critical roles. These findings invite further research
and suggest that the USPTO’s efforts to improve efficiency may need to
look beyond network centrality to other operational or organizational
strategies.
