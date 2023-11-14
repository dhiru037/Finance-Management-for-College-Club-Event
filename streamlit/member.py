import mysql.connector
import streamlit as st
import pandas as pd

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "dhiru038",
    database = "project"
)
mycursor = mydb.cursor()
print("Connection Established")

def app():
    mycursor.execute("select * from participants")
    result=mycursor.fetchall()
    event_id=st.sidebar.text_input("Enter Event ID")
    if st.sidebar.button("Enter"):
        st.title("Welcome to Registration Portal")
        tab1, tab2 = st.tabs(["Registrations","Participants"])
        with tab1:
            st.header("Registrations")
            sql="select * from transactions where type='Register' and event_id=%s"
            mycursor.execute(sql,(event_id,))
            result2=mycursor.fetchall()
            mydb.commit()
            mycursor.close()
            mydb.close()

            trans_id=[item[0] for item in result2]
            types=[item[1] for item in result2]
            dates=[item[2] for item in result2]
            modes=[item[3] for item in result2]
            amounts=[item[4] for item in result2]
            remarks=[item[5] for item in result2]

            data1 = pd.DataFrame({
            'Transaction ID': trans_id,
            'Type': types,
            'Date':dates,
            'Mode': modes,
            'Amount': amounts,
            'Remarks': remarks,
            })
            st.table(data1)
            st.divider()
            #st.button("CLick")
        with tab2:
            st.header("Participants list")
            srns=[item[0] for item in result]
            names=[item[1] for item in result]
            phone=[item[2] for item in result]
            emails=[item[3] for item in result]
            trans_ids=[item[4] for item in result]
            data=pd.DataFrame({
                'SRN':srns,
                'Name':names,
                'Phone No':phone,
                'Email':emails,
                'Transaction ID':trans_ids
            })
            st.table(data)


if __name__ == "__main__":
    app()