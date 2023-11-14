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

budget=0.0
event_name=''
event_venue=''
event_date=''
mycursor.execute("select * from event")
result = mycursor.fetchall()

mycursor.execute("call CalculateDomainFinances()")
result1 = mycursor.fetchall()
#print(result1)
domains=[item[0] for item in result1]
#print(domains)
sub_budgets=[item[1] for item in result1]
incomes=[item[2] for item in result1]
total_income=sum(incomes)
expenditures=[item[3] for item in result1]
total_expenditure=sum(expenditures)
reserves_left=[item[4] for item in result1]
total_reserves=0.0

mycursor.close()
mydb.close()



def update_allocation(dom_id,sub_budget):
    
    mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "dhiru038",
    database = "project"
    )
    mycursor = mydb.cursor()

    
    sql="call update_budget(%s,%s)"
    val=(dom_id,sub_budget)
    mycursor.execute(sql,val)
    mydb.commit()

    mycursor.close()
    mydb.close()

def app():
    st.title("Welcome to the Club Financials, Club Head!")
    
    


    event_id = st.text_input("**Event ID**")
    
    if event_id:
        for item in result:
            if item[0]==event_id:
                event_name=item[1]
                event_venue=item[2]
                event_date=str(item[3])
                budget=float(item[-1])
                total_reserves=budget+float(total_income-total_expenditure)
                
        col1, col2 = st.columns([3,1])
        with col1:
            tab1, tab2, tab3, tab4 = st.tabs(["**Event Details**","**Overall**", "**Domain**","**Stats**"])
            with tab1:
                with st.container():
                    st.header(":violet[Event Details: ]")
                    st.subheader(":blue[ID:] "+event_id)
                    st.subheader(":blue[Name:] "+event_name)
                    st.subheader(":blue[Date:] "+event_date)
                    st.subheader(":blue[Venue:] "+event_venue)
                    st.subheader(f":blue[Allocated budget:] {budget:.2f}")
                    st.divider()
            with tab2:
                st.header("Overall Club Financials")
                data = pd.DataFrame({
                    'Domain': domains,
                    'Allocated Budget': sub_budgets,
                    'Revenue':incomes,
                    'Expenses': expenditures,
                    'Reserves Left': reserves_left
                })
                st.table(data)

                option=st.sidebar.selectbox("**Allocation**",("Update Allocation",),index=None,placeholder="Select operation") 
                if option=="Update Allocation":
                    dom_id_update=st.text_input("Enter Domain ID")
                    new_sub_budget=st.text_input("Enter Sub-Budget")
                    if st.button("Allocate"):
                        update_allocation(dom_id_update,new_sub_budget) 
                        st.success("Budget Updated!")  
                        
                
            
            with tab3:
                st.header("Domain Transactions")
                option=st.selectbox("**Domain**",domains,index=None, placeholder="Choose a domain")

                if option:
                    mydb = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "dhiru038",
                    database = "project"
                    )
                    mycursor = mydb.cursor()
                    mycursor.execute("select trans_id, type, date, mode, amount, remarks from transactions where domain_id = %s;",(option,))
                    result2=mycursor.fetchall()
                    mydb.commit()
                    #print(result2)

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

                    mycursor.close()
                    mydb.close()

                    operation=st.sidebar.selectbox("Domain Financial Operations",("Record Transaction","Delete Transaction"),index=None,placeholder="Select CRUD Operation")
                    if operation=="Record Transaction":
                        with st.form("Record_Transaction"):
                            st.write("Enter New Transaction details")
                            new_trans_id=st.text_input("ID",help="Enter Unique Transaction ID")
                            if new_trans_id in trans_id:
                                st.error("Transaction ID exists!")

                            if option=="LOG":
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
                                val=(new_trans_id,new_trans_type,new_trans_date,new_trans_mode,new_trans_amount,new_trans_remarks,option,event_id)
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


                    elif operation=="Delete Transaction":
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
            with tab4:
                st.subheader("Domain with Highest Revenue:")
                mydb = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "dhiru038",
                database = "project"
                )
                mycursor = mydb.cursor()
                mycursor.execute("""
                    SELECT d.domain_id, d.headed_by, t.total_amount
                    FROM domain d
                    JOIN (
                        SELECT domain_id, SUM(amount) AS total_amount
                        FROM transactions
                        WHERE type IN ('register', 'sponsor')
                        GROUP BY domain_id
                        ORDER BY total_amount DESC
                        LIMIT 1
                    ) t ON d.domain_id = t.domain_id;
                """)
                highest_revenue=mycursor.fetchall()
                mycursor.close()
                mydb.close()
                st.table(highest_revenue)
                st.divider()
                st.subheader("Domain with Highest Expenditure:")
                mydb = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "dhiru038",
                database = "project"
                )
                mycursor = mydb.cursor()
                mycursor.execute("""
                    SELECT d.domain_id, d.headed_by, t.total_amount
                    FROM domain d
                    JOIN (
                        SELECT domain_id, SUM(amount) AS total_amount
                        FROM transactions
                        WHERE type = 'expenditure'
                        GROUP BY domain_id
                        ORDER BY total_amount DESC
                        LIMIT 1
                    ) t ON d.domain_id = t.domain_id;
                """)
                highest_expenditure=mycursor.fetchall()
                mycursor.close()
                mydb.close()
                st.table(highest_expenditure)

        with col2:
            st.markdown(f'<div style="text-align: center; width: 100px; height: 100px; background-color: #F93030; border-radius: 50%; color: white; line-height: 100px; font-size: 20px;">{event_id}</div>', unsafe_allow_html=True)
            st.divider()
            st.write(f":blue[**Total Allocated Budget:**] **{budget:.2f}**")
            st.divider()
            st.write(f":blue[**Total Revenue:**] **{total_income:.2f}**")
            st.divider()
            st.write(f":blue[**Total Expenditure:**] **{total_expenditure:.2f}**")
            st.divider()
            st.write(f":blue[**Total Reserves Left:**] **{total_reserves:.2f}**")
            st.divider()

if __name__ == "__main__":
    app()