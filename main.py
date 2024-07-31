import streamlit as st
import os
import pandas as pd
import random

# make 2 columns
col1, col2 = st.columns(2)

with col1:

    st.title("Créer une nouvelle classe")

    reset_btn = st.button("Supprimer la class en passé")
    if reset_btn:
        # delete the csv of the past class
        if os.path.isfile("./data/class.csv") == True:
            os.remove("./data/class.csv")
        st.text("Le derrier classe est supprimé")

    # read or make dataframe
    if os.path.isfile("./data/class.csv") == True:
        df = pd.read_csv("./data/class.csv", usecols=["NOM", "LANGUE"])

    else:
        df = pd.DataFrame([{"NOM": "AJOUTER NOM ICI", "LANGUE": "AJOUTER LANGUE ICI"}])
    df = st.data_editor(df, num_rows="dynamic") # make df as an editable df

    finish_btn = st.button("finir")
    if finish_btn:
        if os.path.isfile("./data/class.csv") == True:
            os.remove("./data/class.csv")
        df.to_csv("./data/class.csv")

with col2:
    st.title("Faire des groupes des languages differentes")
    # set the number of the members in group
    num_mem = st.number_input("Le numero de personnes par chaque groupe", value = 1)

    # making the group
    if st.button("Faire les groupes"):
        num_stu = len(df)
        # define number of the groups
        if num_stu % num_mem == 0:
            num_gro = int(num_stu / num_mem)
        else:
            num_gro = int(num_stu / num_mem) + 1
        st.text(f"Le numero des groupes est {num_gro}")

        columns = [f"Group{i+1}" for i in range(num_gro)]
        df_group = pd.DataFrame(index=range(num_mem), columns=columns)

        # create temporal df
        df_temp = df.copy()

        # Sort the students
        list_stu = []

        for i in range(len(df)):
            if len(df_temp) > 0:

                stu_index = random.randint(0, len(df_temp)-1)
                stu_name = df_temp.at[stu_index, "NOM"]
                stu_langue = df_temp.at[stu_index, "LANGUE"]

                # if the language of the students have multiple students
                lan_filtered_df = df_temp[df_temp['LANGUE'] == stu_langue]
                if len(lan_filtered_df) >= 2:
                    # make a list for the students speak same language
                    lan_filtered_list = lan_filtered_df['NOM'].tolist()
                    shuffled_lan_filtered_list = random.sample(lan_filtered_list, len(lan_filtered_list))

                    list_stu.extend(shuffled_lan_filtered_list)

                    # delete students
                    df_temp = df_temp[df_temp["LANGUE"] != stu_langue]
                # if the language of the student is spoken just by this student
                else:
                    # add student name to the list
                    list_stu.append(stu_name)
                    # delete student info
                    df_temp.drop(stu_index, inplace=True)


                df_temp.reset_index(drop=True, inplace=True)

        # register students to df_group
        i = 0
        for ind in range(num_mem):
            for col in range(num_gro):
                if i < len(list_stu):
                    df_group.iat[ind, col] = list_stu[i]
                    i += 1

        # display the result
        st.dataframe(df_group)


