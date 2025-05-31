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
    ## Ncells  4705823 251.4    8314865 444.1  5130626 274.1
    ## Vcells 49885984 380.6   95874234 731.5 80201731 611.9

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
    ## Ncells  4797230 256.2    8314865 444.1  6845032 365.6
    ## Vcells 52072990 397.3   95874234 731.5 95599212 729.4

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
    ## Ncells  4803686 256.6   15094977  806.2  15094977  806.2
    ## Vcells 64434835 491.6  138234896 1054.7 138087735 1053.6

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

-Group 172 is composed of experienced examiners with an average tenure
of over 15 years, indicating long-term involvement in patent application
reviews. The group has managed a broad spectrum of patent applications
for nearly two decades, with examiners distributed across at least nine
different art units within class 172, reflecting a varied workload with
diverse outcomes.

-Group 175 consists of patent examiners whose collective expertise is
showcased by an average tenure of over 15 years. With a steady stream of
patent applications dating back to the start of 2000, this group has
demonstrated consistent engagement in patent processing. Examiners in
group 175 cover a spectrum of art units ranging from 1751 to 1759,
pointing to a diversity of specialties and a breadth of workload. The
median filing date of June 2004 suggests a peak period of activity
mid-way through the range of their recorded history.

-Groups 172 and 175 both exhibit long-term dedication and expertise in
patent examination, having processed applications for nearly two decades
within the same technology center. Despite their shared commitment and
organizational context, they differ in their peak periods of activity,
with group 172 showing a later median filing date, indicating possibly
different workflows or shifts in application volume over time.
Additionally, each group operates across a distinct range of art units,
reflecting varied areas of specialization.

# Histograms for gender and race

    par(mfrow=c(1,2))

    plot1 <- ggplot(group_172, aes(x = factor(gender))) +
      geom_bar(fill="darkblue") +
      ggtitle("Work Group 172")

    plot2 <- ggplot(group_175, aes(x = factor(gender))) +
      geom_bar(fill="darkred") +
      ggtitle("Work Group 175")

    grid.arrange(plot1, plot2, ncol=2)

![](Exercise3_files/figure-markdown_strict/unnamed-chunk-18-1.png) -The
Gender distribution bar plots for groups 172 and 175 indicate that both
groups have more male than female examiners, with group 172 displaying a
significantly wider gender gap. Additionally, group 172 has a larger
overall number of examiners. Both groups have a similar count of
unspecified gender data.

    par(mfrow=c(1,2))

    plot1 <- ggplot(group_172, aes(x = factor(race))) +
      geom_bar(fill="darkblue") +
      ggtitle("Work Group 172")

    plot2 <- ggplot(group_175, aes(x = factor(race))) +
      geom_bar(fill="darkred") +
      ggtitle("Work Group 175")

    grid.arrange(plot1, plot2, ncol=2)

![](Exercise3_files/figure-markdown_strict/unnamed-chunk-19-1.png) -The
racial composition bar charts for groups 172 and 175 illustrate that
both groups are predominantly white, with a smaller presence of Asian,
black, and Hispanic individuals. However, group 172 shows a much larger
overall racial diversity, with a substantially higher count of white
individuals compared to the other racial categories. In contrast, group
175 has a more balanced distribution among the non-white categories,
particularly with a relatively higher count of Asians, indicating more
racial diversity within the group.

## 3. Create advice networks from `edges_sample` and calculate centrality scores

## for examiners in your selected workgroups

### Pick measure(s) of centrality you want to use and justify your choice

### Characterize and discuss the relationship between centrality and other examiners’

### characteristics

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

### Calculate centrality scores

    Degree <- degree(advice_net, v=V(advice_net))
    Betweenness <- betweenness(advice_net)
    Closeness <- closeness(advice_net)

### Visualize centralities

    # save centrality scores
    V(advice_net)$size = Degree
    V(advice_net)$clos = round(Closeness,2)
    V(advice_net)$bet = round(Betweenness,2)
    # color by art unit
    V(advice_net)$color = nodes$art_unit

    # save scores in a data frame for easy visualization
    centralities <- cbind(Degree, Closeness, Betweenness)
    centralities = round(centralities,2)
    centralities = data.frame(centralities)

    # plot graph 
    ggraph(advice_net, layout="kk") +
           geom_edge_link()+
           geom_node_point(aes(size=size, color=color), show.legend=T) 

![](Exercise3_files/figure-markdown_strict/unnamed-chunk-23-1.png)

    # plot final graph 
    ggraph(advice_net, layout="kk") +  
      geom_edge_link(alpha = 0.2) +  
      geom_node_point(aes(size=size, color=as.factor(color)), show.legend=TRUE) +
      scale_color_discrete(name = "Art Unit") +  
      geom_node_text(aes(label = name), check_overlap = TRUE, size = 3) +  
      theme(legend.position = "right") +
      ggtitle("Advice Network for Work Group 172 and 175")  

![](Exercise3_files/figure-markdown_strict/unnamed-chunk-24-1.png) -The
advice network for work groups 172 and 175 reveals intricate patterns of
mentorship and consultation. Specifically, Examiner ‘67829’ from group
172 stands out as a highly interconnected node, suggesting a significant
role in providing guidance within this group. This central position may
point to a senior or highly regarded status, with a broad influence over
the group’s intellectual and decision-making processes. In contrast,
Examiner ‘98852’ from group 175 appears to bridge across the groups,
hinting at a collaborative role that transcends the confines of their
primary group, potentially fostering innovation and cross-group synergy.
This visualization captures the essence of the advisory dynamics,
highlighting key players in knowledge exchange and the vital links that
support a cohesive, yet diverse, organizational knowledge structure.

-In examining the centrality of examiners within the network, focusing
on degree centrality and betweenness centrality is pertinent as they
provide insights into an examiner’s connectivity and their role as a
bridge between others, respectively. Closeness centrality, however, may
be less relevant in this context as it primarily measures an examiner’s
proximity to other examiners in terms of the shortest paths, which may
not necessarily reflect their influence or importance within the broader
network of advice exchange.

    # show info for the first examiner being discussed
    first_examiner <- applications %>% 
      filter(examiner_id==67829)
    summary(first_examiner)

    ##  application_number  filing_date         examiner_name_last examiner_name_first
    ##  Length:520         Min.   :2000-06-06   Length:520         Length:520         
    ##  Class :character   1st Qu.:2003-03-22   Class :character   Class :character   
    ##  Mode  :character   Median :2005-05-30   Mode  :character   Mode  :character   
    ##                     Mean   :2007-09-09                                         
    ##                     3rd Qu.:2012-01-27                                         
    ##                     Max.   :2017-02-14                                         
    ##                                                                                
    ##  examiner_name_middle  examiner_id    examiner_art_unit  uspc_class       
    ##  Length:520           Min.   :67829   Min.   :1728      Length:520        
    ##  Class :character     1st Qu.:67829   1st Qu.:1753      Class :character  
    ##  Mode  :character     Median :67829   Median :1757      Mode  :character  
    ##                       Mean   :67829   Mean   :1767                        
    ##                       3rd Qu.:67829   3rd Qu.:1795                        
    ##                       Max.   :67829   Max.   :1795                        
    ##                                                                           
    ##  uspc_subclass      patent_number      patent_issue_date   
    ##  Length:520         Length:520         Min.   :2005-01-18  
    ##  Class :character   Class :character   1st Qu.:2007-04-17  
    ##  Mode  :character   Mode  :character   Median :2008-06-24  
    ##                                        Mean   :2008-09-26  
    ##                                        3rd Qu.:2010-02-16  
    ##                                        Max.   :2014-08-26  
    ##                                        NA's   :321         
    ##   abandon_date        disposal_type      appl_status_code appl_status_date  
    ##  Min.   :2002-04-15   Length:520         Min.   : 20.0    Length:520        
    ##  1st Qu.:2006-09-28   Class :character   1st Qu.:150.0    Class :character  
    ##  Median :2009-04-30   Mode  :character   Median :161.0    Mode  :character  
    ##  Mean   :2009-12-20                      Mean   :140.5                      
    ##  3rd Qu.:2013-06-17                      3rd Qu.:161.0                      
    ##  Max.   :2016-12-01                      Max.   :250.0                      
    ##  NA's   :307                             NA's   :7                          
    ##        tc          gender              race           earliest_date       
    ##  Min.   :1700   Length:520         Length:520         Min.   :2000-06-06  
    ##  1st Qu.:1700   Class :character   Class :character   1st Qu.:2000-06-06  
    ##  Median :1700   Mode  :character   Mode  :character   Median :2000-06-06  
    ##  Mean   :1700                                         Mean   :2000-06-06  
    ##  3rd Qu.:1700                                         3rd Qu.:2000-06-06  
    ##  Max.   :1700                                         Max.   :2000-06-06  
    ##                                                                           
    ##   latest_date          tenure_days  
    ##  Min.   :2017-05-19   Min.   :6191  
    ##  1st Qu.:2017-05-19   1st Qu.:6191  
    ##  Median :2017-05-19   Median :6191  
    ##  Mean   :2017-05-19   Mean   :6191  
    ##  3rd Qu.:2017-05-19   3rd Qu.:6191  
    ##  Max.   :2017-05-19   Max.   :6191  
    ## 

    # show info for the second examiner being discussed
    second_examiner <- applications %>% 
      filter(examiner_id==98852)
    summary(second_examiner)

    ##  application_number  filing_date         examiner_name_last examiner_name_first
    ##  Length:1283        Min.   :2000-01-03   Length:1283        Length:1283        
    ##  Class :character   1st Qu.:2002-11-13   Class :character   Class :character   
    ##  Mode  :character   Median :2006-02-27   Mode  :character   Mode  :character   
    ##                     Mean   :2007-03-22                                         
    ##                     3rd Qu.:2011-12-11                                         
    ##                     Max.   :2017-01-25                                         
    ##                                                                                
    ##  examiner_name_middle  examiner_id    examiner_art_unit  uspc_class       
    ##  Length:1283          Min.   :98852   Min.   :1723      Length:1283       
    ##  Class :character     1st Qu.:98852   1st Qu.:1742      Class :character  
    ##  Mode  :character     Median :98852   Median :1754      Mode  :character  
    ##                       Mean   :98852   Mean   :1754                        
    ##                       3rd Qu.:98852   3rd Qu.:1754                        
    ##                       Max.   :98852   Max.   :1795                        
    ##                                                                           
    ##  uspc_subclass      patent_number      patent_issue_date   
    ##  Length:1283        Length:1283        Min.   :2001-10-16  
    ##  Class :character   Class :character   1st Qu.:2005-07-08  
    ##  Mode  :character   Mode  :character   Median :2009-10-20  
    ##                                        Mean   :2009-10-04  
    ##                                        3rd Qu.:2013-10-11  
    ##                                        Max.   :2017-06-20  
    ##                                        NA's   :583         
    ##   abandon_date        disposal_type      appl_status_code appl_status_date  
    ##  Min.   :2001-03-06   Length:1283        Min.   : 30.0    Length:1283       
    ##  1st Qu.:2006-05-02   Class :character   1st Qu.:150.0    Class :character  
    ##  Median :2008-12-24   Mode  :character   Median :161.0    Mode  :character  
    ##  Mean   :2009-05-20                      Mean   :159.5                      
    ##  3rd Qu.:2012-07-21                      3rd Qu.:161.0                      
    ##  Max.   :2017-03-10                      Max.   :250.0                      
    ##  NA's   :809                             NA's   :1                          
    ##        tc          gender              race           earliest_date       
    ##  Min.   :1700   Length:1283        Length:1283        Min.   :2000-01-03  
    ##  1st Qu.:1700   Class :character   Class :character   1st Qu.:2000-01-03  
    ##  Median :1700   Mode  :character   Mode  :character   Median :2000-01-03  
    ##  Mean   :1700                                         Mean   :2000-01-03  
    ##  3rd Qu.:1700                                         3rd Qu.:2000-01-03  
    ##  Max.   :1700                                         Max.   :2000-01-03  
    ##                                                                           
    ##   latest_date          tenure_days  
    ##  Min.   :2017-05-23   Min.   :6350  
    ##  1st Qu.:2017-05-23   1st Qu.:6350  
    ##  Median :2017-05-23   Median :6350  
    ##  Mean   :2017-05-23   Mean   :6350  
    ##  3rd Qu.:2017-05-23   3rd Qu.:6350  
    ##  Max.   :2017-05-23   Max.   :6350  
    ## 

    first_examiner

    ## # A tibble: 520 × 21
    ##    application_number filing_date examiner_name_last examiner_name_first
    ##    <chr>              <date>      <chr>              <chr>              
    ##  1 09589042           2000-06-06  BARTON             JEFFREY            
    ##  2 09612829           2000-07-07  BARTON             JEFFREY            
    ##  3 09633172           2000-08-04  BARTON             JEFFREY            
    ##  4 09647004           2000-11-29  BARTON             JEFFREY            
    ##  5 09647910           2000-12-07  BARTON             JEFFREY            
    ##  6 09689010           2000-10-12  BARTON             JEFFREY            
    ##  7 09760239           2001-01-13  BARTON             JEFFREY            
    ##  8 09762519           2001-02-07  BARTON             JEFFREY            
    ##  9 09768075           2001-01-23  BARTON             JEFFREY            
    ## 10 09780230           2001-02-09  BARTON             JEFFREY            
    ## # ℹ 510 more rows
    ## # ℹ 17 more variables: examiner_name_middle <chr>, examiner_id <dbl>,
    ## #   examiner_art_unit <dbl>, uspc_class <chr>, uspc_subclass <chr>,
    ## #   patent_number <chr>, patent_issue_date <date>, abandon_date <date>,
    ## #   disposal_type <chr>, appl_status_code <dbl>, appl_status_date <chr>,
    ## #   tc <dbl>, gender <chr>, race <chr>, earliest_date <date>,
    ## #   latest_date <date>, tenure_days <dbl>

    second_examiner

    ## # A tibble: 1,283 × 21
    ##    application_number filing_date examiner_name_last examiner_name_first
    ##    <chr>              <date>      <chr>              <chr>              
    ##  1 09269214           2000-03-21  WILKINS III        HARRY              
    ##  2 09462486           2000-04-07  WILKINS III        HARRY              
    ##  3 09476664           2000-01-03  WILKINS III        HARRY              
    ##  4 09485339           2000-05-15  WILKINS III        HARRY              
    ##  5 09486948           2000-03-06  WILKINS III        HARRY              
    ##  6 09490267           2000-01-24  WILKINS III        HARRY              
    ##  7 09492139           2000-01-27  WILKINS III        HARRY              
    ##  8 09492347           2000-01-27  WILKINS III        HARRY              
    ##  9 09492552           2000-01-27  WILKINS III        HARRY              
    ## 10 09493990           2000-01-28  WILKINS III        HARRY              
    ## # ℹ 1,273 more rows
    ## # ℹ 17 more variables: examiner_name_middle <chr>, examiner_id <dbl>,
    ## #   examiner_art_unit <dbl>, uspc_class <chr>, uspc_subclass <chr>,
    ## #   patent_number <chr>, patent_issue_date <date>, abandon_date <date>,
    ## #   disposal_type <chr>, appl_status_code <dbl>, appl_status_date <chr>,
    ## #   tc <dbl>, gender <chr>, race <chr>, earliest_date <date>,
    ## #   latest_date <date>, tenure_days <dbl>

-Jeffrey Thomas Barton, Examiner ‘67829’, a white male, has exemplified
a profound commitment to the patent examination field from June 6, 2000,
to May 19, 2017, accumulating nearly 17 years of service. Throughout his
tenure, Barton has demonstrated remarkable versatility, engaging with a
broad range of art units from 1728 to 1795. The zenith of his patent
application activity around mid-2008, complemented by a wide array of
disposal outcomes and application statuses, underscores his deep-seated
expertise and pronounced impact on the patent examination community. His
substantial experience is further highlighted by his position as the
individual with the highest degree centrality in the advice network,
indicating his central role in the dissemination of knowledge and
advice. Barton’s long-standing service, underpinned by extensive
technical knowledge and procedural acumen, establishes him as a pivotal
figure and a seasoned professional within the patent examination
landscape, vital for fostering collaboration and guiding decision-making
processes.

-Harry D Wilkins III, Examiner ‘98852’, a white male, has demonstrated a
steadfast commitment to the patent examination field from January 3,
2000, to May 23, 2017, marking over 17 years of dedicated service.
Throughout his tenure, Wilkins has been instrumental across art units
from 1723 to 1795, showcasing his ability to bridge diverse specialties.
Notably, his role is amplified by having the highest betweenness
centrality in the advice network, positioning him as a pivotal connector
and advisor within the patent examination community. His activities,
notably peaking in February 2006, reflect a broad impact, characterized
by a variety of patent examination outcomes. Wilkins’ unique stance in
the advice network, coupled with his extensive experience, cements his
status as a seasoned professional, vital in driving cross-disciplinary
engagement and fostering an environment of collaboration and innovation.

-Jeffrey Thomas Barton and Harry D Wilkins III serve as pillars of
expertise and collaboration within their respective realms, embodying
different facets of influence. Barton’s role is marked by his
significant contributions to the core activities within his area,
mirroring a leadership style deeply rooted in specialized knowledge and
hands-on involvement. Conversely, Wilkins emerges as a vital connector
for inter-departmental interactions, with his strategic position
enabling key dialogues across various segments, showcasing a leadership
model that emphasizes the importance of connectivity and
cross-disciplinary partnerships. Their activities highlight distinct
phases of impactful engagement, illustrating the diverse ways in which
leadership manifests within complex networks. Barton is viewed as a
mentor within his circle, whereas Wilkins acts as a facilitator for
essential inter-unit discourse, collectively enhancing the
organizational ecosystem’s cohesion and innovative potential.

-Both Barton and Wilkins, as white males, possess extensive tenure
spanning over 17 years each in the patent examination domain. This
shared attribute underscores their deep-rooted experience and longevity
within their respective roles. Their extended service not only signifies
their dedication and commitment to their profession but also suggests a
wealth of accumulated knowledge and expertise over time. This
commonality reflects a broader demographic trend within the patent
examination field and emphasizes the historical context within which
their careers have evolved. Despite their individual differences in
network centrality and approach, their shared demographic background and
extensive tenure serve as foundational elements shaping their roles and
contributions within the organization.
