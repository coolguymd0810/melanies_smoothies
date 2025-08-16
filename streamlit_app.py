# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session

import requests


# Write directly to the app
st.title(f"Customize Your Smoothie")

name_on_order = st.text_input("My Parent new Healthy Diner")
st.write("The Name on your Smoothie will be: ", name_on_order)


st.write(
  """Choose the Fruits,you want to custmoize !!
  """
)

from snowflake.snowpark.functions import col

#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe , use_container_width = True)
st.stop()

ingredients_list = st.multiselect (
    'Choose up to 5 ingredients'
    , my_dataframe
    , max_selections=5
    
)
ingredients_string = ''

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen )
        sf_df = st.dataframe (data= smoothiefroot_response.json(),use_container_width = True) 
    st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
    values ('""" + ingredients_string + """' , '""" + name_on_order + """')""" 
    
    #st.write(my_insert_stmt)

    if st.button('Submit Order'):        
        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")


