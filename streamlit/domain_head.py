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

event_id=st.sidebar.text_input("Event ID")
member_id=st.sidebar.text_input("Member ID")
mycursor.execute("select domain_id, domain_name, sub_budget from domain where headed_by = %s",(member_id,))
result = mycursor.fetchall()

if result:
    domain_id=result[0][0]
    domain_name=result[0][1]
    sub_budget=float(result[0][2])


mycursor.close()
mydb.close()


def domain_transactions():
    mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "dhiru038",
    database = "project"
    )
    mycursor = mydb.cursor()

    mycursor.execute("select * from transactions where domain_id = %s",(domain_id,))
    result1 = mycursor.fetchall()

    mycursor.close()
    mydb.close()
    return result1


def domain_totals():
    mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "dhiru038",
    database = "project"
    )
    mycursor = mydb.cursor()
    mycursor.execute("select domain_income(%s)",(domain_id,))
    total_revenue=mycursor.fetchall()
    mycursor.execute("select domain_expenditure(%s)",(domain_id,))
    total_expenditure=mycursor.fetchall()
    result3=[total_revenue,total_expenditure]
    #print(result3)
    return result3

def app():

    if st.sidebar.button("Enter domain"):
        st.title("Welcome to your Domain,")
        st.title("Head of "+str(domain_name))

        col1, col2 = st.columns([3,1])
        with col1:
            tab1, tab2 = st.tabs(["**Domain Details**","**Domain Transactions**"])
            with tab1:
                with st.container():
                    st.header(":violet[Domain Details: ]")
                    st.subheader(":blue[ID:] "+domain_id)
                    st.subheader(":blue[Name:] "+domain_name)
                    st.subheader(":blue[Allocated Budget:] "+str(sub_budget))
                    st.subheader(":blue[Headed By:] "+member_id)
                    st.divider()
                    #st.button("click")
            with tab2:
                st.header("Domain Transactions")
                result2=domain_transactions()
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

                #mycursor.close()
                #mydb.close()

                tab11, tab22 = st.tabs(["Record Transaction","Delete Transaction"])
                with tab11:
                    with st.form("Record_Transaction"):
                        st.write("Enter New Transaction details")
                        new_trans_id=st.text_input("ID",help="Enter Unique Transaction ID")
                        if new_trans_id in trans_id:
                            st.error("Transaction ID exists!")

                        if domain_id=="LOG":
                            new_trans_type=st.selectbox("Type",("Register","Expenditure","Sponsor"),index=None,placeholder="Choose type")
                        else:
                            new_trans_type=st.selectbox("Type",("Expenditure","Sponsor"),index=None,placeholder="Choose type")

                        new_trans_date=st.date_input("Date")
                        new_trans_amount=st.text_input("Amount")
                        new_trans_mode=st.selectbox("Mode of Payment",("Cash","Online","Check"),index=None,placeholder="Choose payment method")
                        new_trans_remarks=st.text_input("Remarks")          

                        submitted = st.form_submit_button("Record")
                        if submitted:
                            mydb = mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "dhiru038",
                            database = "project"
                            )
                            mycursor = mydb.cursor()
                            sql=("insert into transactions values(%s,%s,%s,%s,%s,%s,%s,%s)")
                            val=(new_trans_id,new_trans_type,new_trans_date,new_trans_mode,new_trans_amount,new_trans_remarks,domain_id,event_id)
                            mycursor.execute(sql,val)
                            mydb.commit()
                            st.success("Record Inserted!")
                            mycursor.close()
                            mydb.close()
                    
                    if new_trans_type=="Register":
                        with st.form("Participant details"):
                            st.write("Enter Participant details")
                            new_srn=st.text_input("SRN")
                            new_name=st.text_input("Name")
                            new_phone=st.text_input("Phone")
                            new_email=st.text_input("Email")
                            submitted1 = st.form_submit_button("Register Participant")
                            if submitted1:
                                mydb = mysql.connector.connect(
                                host = "localhost",
                                user = "root",
                                password = "dhiru038",
                                database = "project"
                                )
                                mycursor = mydb.cursor()
                                sql=("insert into participants values(%s,%s,%s,%s,%s)")
                                val=(new_srn,new_name,new_phone,new_email,new_trans_id)
                                mycursor.execute(sql,val)
                                mydb.commit()
                                st.success("Participant Registered!")

                                mycursor.close()
                                mydb.close()

                with tab22:
                    st.write("Deleting a Transaction")
                    del_trans_id=st.text_input("Transaction ID to be deleted")
                    if st.button("Delete"):
                        mydb = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        password = "dhiru038",
                        database = "project"
                        )
                        mycursor = mydb.cursor()
                        mycursor.execute("delete from transactions where trans_id = %s",(del_trans_id,))
                        mydb.commit()
                        st.success("Transaction Deleted!")

                        mycursor.close()
                        mydb.close()

            with col2:
                st.markdown(f'<div style="text-align: center; width: 100px; height: 100px; background-color: #F93030; border-radius: 50%; color: white; line-height: 100px; font-size: 20px;">{event_id}</div>', unsafe_allow_html=True)
                st.divider()
                st.write(f":blue[**Allocated Budget:**] **{sub_budget:.2f}**")
                st.divider()
                result3=domain_totals()
                #print(result3)
                total_revenue=result3[0][0][0]
                total_expenditure=result3[1][0][0]
                #print(total_revenue,total_expenditure)
                st.write(f":blue[**Total Revenue:**] **{total_revenue:.2f}**")
                st.divider()
                st.write(f":blue[**Total Expenditure:**] **{total_expenditure:.2f}**")
                st.divider()
                total_reserves=float(sub_budget)+float(total_revenue-total_expenditure)
                st.write(f":blue[**Total Reserves Left:**] **{total_reserves:.2f}**")
                st.divider()
if __name__ == "__main__":
    app()