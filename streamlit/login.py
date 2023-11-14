import mysql.connector
import streamlit as st
import subprocess



mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "dhiru038",
    database = "project"
)
mycursor = mydb.cursor()
print("Connection Established")



def app():

    mycursor.execute("select * from member")
    result = mycursor.fetchall()
    mem_id_list=[]
    #print(result)
    mem_id_list = [item[0] for item in result]
    
    mycursor.execute("select headed_by, domain_id from domain")
    dom_head_list = mycursor.fetchall()

    st.title(":violet[Finance Management for College Club Events]")
    st.subheader("Login / Sign Up")
    option = st.sidebar.radio("Choose", ["Login", "Sign Up"],key="option")

    member_id = st.text_input("Member ID", help="Enter your unique member ID")
    name = st.text_input("Name")
    domain_id = st.text_input("Domain ID")

    mycursor.execute("SELECT domain_name FROM domain WHERE domain_id = %s",(domain_id,))
    dom_name = str(mycursor.fetchone())
    
    if option=="Sign Up":
        
        if st.button("Sign Up"):
            
            
            if member_id in mem_id_list:
                st.error("Member already exists!")

            else:
                sql = "insert into member values(%s,%s,%s)"
                val = (member_id,name,domain_id)
                mycursor.execute(sql,val)
                mydb.commit()
                st.success("Signed Up!")
            

    else:
        
        tuple1 = (member_id,name,domain_id)
        dom_head_check=(member_id, domain_id)
        if st.button("Login"):
            if tuple1 in result:
                st.success("Logged In!")
                if domain_id == 'HEAD':
                    st.header("Welcome to Club Financials, Club Head!")
                    st.subheader("Name : "+name)
                    st.subheader("Member ID : "+member_id)
                    subprocess.run(["streamlit", "run", "club_head.py"])


                elif dom_head_check in dom_head_list:
                    

                    st.header("Welcome to Domain Financials, Head of "+dom_name)
                    st.subheader("Name : "+name)
                    st.subheader("Member ID : "+member_id)
                    subprocess.run(["streamlit", "run", "domain_head.py"])
                else:
                    st.header("Welcome!")
                    st.subheader("Name : "+name)
                    st.subheader("Member ID : "+member_id)
                    subprocess.run(["streamlit", "run", "member.py"])

            elif tuple1[0] in mem_id_list:
                st.error("Check credentials!")

            else:
                st.error("Please sign up first!")
           
if __name__ == "__main__":
    app()