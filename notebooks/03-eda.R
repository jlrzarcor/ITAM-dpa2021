source("utils.R", encoding = 'UTF-8')



## UNIVARIATE. Selecting Plots

a_univariate <- function(df = foodinsp_data, var_cols = c('all'),
                         numvar_hist_box = 'hist',
                         num_bin_his = 37){
  ## Discriminate numerical and categorical variables.
  St1<- left_join(as_tibble(var_cols), foodinsp_coltype,
                  by = c("value" = "varname"))
  num_tag <- as.vector(St1 %>% filter(vartype == "numeric")) %>% pull(value)
  cat_tag <- as.vector(St1 %>% filter(vartype == "character" |
                                        vartype == "factor")) %>% pull(value)

  ## Evaluate if all categories are selected or subselect by cat and num.
  if(is.null(var_cols) || var_cols[[1]] == 'all'){
    subdf_num <- df %>% select_if(is.numeric) %>% as.data.frame()
    subdf_fct <- df %>% select_if(is.factor) %>%
      cbind(df %>% select_if(is.character)) %>%  as.data.frame() %>%
      pivot_longer(cols =  everything(.), values_to = "categ_value",
                   names_to = "categorical") %>%
      group_by(categorical, categ_value) %>%
      dplyr::summarise(count = n()) %>% arrange(desc(count)) %>% ungroup()
    if(numvar_hist_box == "hist"){graf_univ_num_h(subdf_num, num_bin_his)}
    if(numvar_hist_box != "hist"){graf_univ_num_b(subdf_num)}
    graf_univ_fct(subdf_fct)
  }
  else{
    if(length(num_tag)>0){subdf_num <- df %>% select(all_of(num_tag)) %>% as.data.frame()
    if(numvar_hist_box == "hist"){graf_univ_num_h(subdf_num, num_bin_his)}
    if(numvar_hist_box != "hist"){graf_univ_num_b(subdf_num)}
    }
    if(length(cat_tag)>0){subdf_fct <- df %>% select(all_of(cat_tag)) %>%
      pivot_longer(cols =  everything(.), values_to = "categ_value",
                   names_to = "categorical") %>%
      group_by(categorical, categ_value) %>%
      dplyr::summarise(count = n()) %>% arrange(desc(count)) %>% ungroup()
    graf_univ_fct(subdf_fct)}
  }
}





## BIVARIATE. Selecting Plots


b_bivar_splom<- function(df = foodinsp_data, var_cols = c('all')){
  ## Discriminate numerical and categorical variables.
  St1<- left_join(as_tibble(var_cols), foodinsp_coltype,
                  by = c("value" = "varname"))
  num_tag <- as.vector(St1 %>% filter(vartype == "numeric")) %>% pull(value)
  cat_tag <- as.vector(St1 %>% filter(vartype == "character" |
                                        vartype == "factor")) %>% pull(value)

  if(is.null(var_cols) || var_cols[[1]] == 'all'){
    subdf_num <- df %>% select_if(is.numeric) %>% as.data.frame()
    graf_bi_splom(subdf_num)
  }
  else{
    if(length(num_tag)>0){subdf_num <- df %>% select(all_of(num_tag)) %>% as.data.frame()
    graf_bi_splom(subdf_num)}
    ##if(length(cat_tag)>0){return()}
  }
}







## MULTIVARIATE. Selecting Plots
