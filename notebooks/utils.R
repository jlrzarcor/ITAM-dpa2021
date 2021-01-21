
## JZC: ID_F1 --> This function aim to load data if It doesn´t exist
#load <- function(){

#  if(file.exists('imports-85.csv')){saveRDS('imports-85.csv', "foodinsp.rds")}

#  if(!file.exists('imports-85.rds')){
#    foodinsp_url <- 'https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data'

#    foodinsp_data <- read_csv(foodinsp_url,
 #                            col_names = foodinsp_colnames,
  #                           na = 'XXXXXXX')
#    saveRDS(foodinsp_data, "foodinsp.rds")
#    print('foodinsp.rds se bajó y guardó\n')
#  }
#  else{
#    warning('foodinsp.rds ya existe\n')
#    foodinsp_data <- readRDS("foodinsp.rds")
#  }

#  return(foodinsp_data)
#}



## JZC: ID_F2 --> This functions aims to clean data

foodinsp_clean_colnames <- function(x){
  str_replace_all(tolower(x),"/| ",'_')
  str_replace_all(tolower(x),"-",'_')
}

foodinsp_clean_data <- function(x){
  str_replace_all(tolower(x),"-",'_')
}



# JZC: ID_F3 --> NOMBRES DE VARIABLES LIMPIOS Y EN MINÚSCULAS
# Es un vector con los nombres de las columnas, se utiliza en varias funciones

foodinsp_colnames_min <- foodinsp_clean_colnames(foodinsp_colnames)



# JZC: ID_F4 --> DATAFRAME WITH VARIABLE NAMES AND TYPE OF VARIABLE
# Useful to discriminate type of graphing construction

foodinsp_get_coltypes <- function(foodinsp_data) {
  df_var_type <- as.data.frame(sapply(foodinsp_data, class))
  df_var_type <- rownames_to_column(.data = df_var_type, "varname")
  colnames(df_var_type) <- c('varname','vartype')
  df_var_type
}



# ID_F5 --> UNIVARIATE PLOTS: 1 NUMERIC VARS, 2 FCTRS VARS
#This function aim to plot all vars from df by numeric.
#For Numeric vars plots --> boxplot; factor vars --> plot bars.

graf_univ_num_h <- function(data, num_bin_his) {
  plot(ggplot(stack(data), aes(x = values)) +
         geom_histogram(fill = "lightgray", col = "steelblue", bins = num_bin_his) +
         facet_wrap(~ind, scale="free", ncol = 5))

}
graf_univ_num_b <- function(data) {
  plot(ggplot(stack(data), aes(x = ind, y = values)) +
         geom_boxplot(outlier.colour = "red", outlier.size = 2, varwidth = TRUE) +
         facet_wrap(~ind, scale="free", ncol = 7))
}
graf_univ_fct <- function(data) {
  ##return(data)
  plot(ggplot(data, aes(x = reorder(categ_value,count), y = count)) +
         geom_bar(fill = "lightgray", col = "steelblue", stat="identity") +
         coord_flip() +
         ##theme_hc() +
         ylab('conteo') +
         xlab('Valores Variable Categ.') +
         facet_wrap(~categorical, scale="free", ncol = 5) )
}









##********************* UNDER CONSTRUCION *********************##






# ID_F6 --> BIVARIATE PLOTS: 1 NUMERIC VARS, 2 FCTRS VARS
#This function aim to plot all vars from df by numeric.
#For Numeric vars --> ; factor vars --> .

graf_bi_splom <- function(data){
  ggpairs(data = data,
          title="Precio Autos '85 vs Características Mecánicas",
          upper = list(contious='smooth_loess'),
          diag=list(continuous='densityDiag'), axisLabels='none',
          progress = FALSE, proportions = "auto")
}







# ID_F7 --> MULTIVARIATE PLOTS: 1 NUMERIC VARS, 2 FCTRS VARS    REVIEW REVIEW REVIEW
#This function aim to plot all vars from df by numeric.         REVIEW REVIEW REVIEW
#For Numeric vars --> ; factor vars --> .           REVIEW REVIEW REVIEW

