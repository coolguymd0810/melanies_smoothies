# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session

import requests
import pandas as pd


# Write directly to the app
st.title(f"Customize Your Smoothie")

name_on_order = st.text_input("Order Name on Smoothie:")
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
#st.dataframe(data=my_dataframe , use_container_width = True)
#st.stop()

#convert the snowpark df to a pandas df so we can use the LOC function

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()


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

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

      
        st.subheader(fruit_chosen + '- Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on )
        sf_df = st.dataframe (data= smoothiefroot_response.json(),use_container_width = True) 
    st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
    values ('""" + ingredients_string + """' , '""" + name_on_order + """')""" 
    
    #st.write(my_insert_stmt)

    if st.button('Submit Order'):        
        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")


