colnames(foodinsp_data) <- foodinsp_clean_colnames(foodinsp_colnames)
problematic_rows <- problems(foodinsp_data)$row

foodinsp_data <- foodinsp_data %>% mutate_at(c(3),list(foodinsp_clean_data))
foodinsp_data <- readr::type_convert(foodinsp_data, na = '?', trim_ws = TRUE)
foodinsp_data <- readr::type_convert(foodinsp_data)

## Using imports-85.names we can infere and declare categorical vars. a priori
foodinsp_data  <- foodinsp_data %>%
  mutate_at(c(5:6,12:14),list(as.factor))
