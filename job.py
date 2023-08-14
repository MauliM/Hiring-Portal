import streamlit as st
import pandas as pd
import pickle
def correct_type(s):
    make_str = str(s)
    remove_hyphen = make_str.replace("-", "")
    remove_slash = remove_hyphen.replace("/", "")
    return remove_slash.lower()
def recommend(choice):
    job_index = sample[sample["Position"] == choice].index[0]
    job_index = sample.index.get_loc(job_index)
    distances = similarity[job_index]
    jobs_list = sorted(list(enumerate(distances)), reverse=True, key=lambda e: e[1])[1:11]

    jobs = []
    company = []
    city = []
    state = []
    for i in jobs_list:
        jobs.append(sample_csv.iloc[i[0]]["Position"])
        company.append(sample_csv.iloc[i[0]]["Company"])
        city.append(sample_csv.iloc[i[0]]["City"])
        state.append(sample_csv.iloc[i[0]]["State.Name"])
    return jobs, company, city, state


data = pickle.load(open("sample_dict.pkl", "rb"))
sample = pd.DataFrame(data)
similarity = pickle.load(open("similarity.pkl", "rb"))
sample_csv = pd.read_csv("sample_csv.csv")

st.title("Hiring Portal")

pos = st.selectbox("Select Title", ["Which kind of Job are you looking for?"] + list(sample_csv["Position"].unique()))

col1, col2 = st.columns(2)
with col1:
    sta = st.selectbox("Select State",["Select State"] + sorted(list(sample_csv["State.Name"].unique())))
with col2:
    specific_cities = sample_csv[sample_csv["State.Name"] == sta]
    ci = st.selectbox("Select City", ["Select City"] + sorted(list(specific_cities["City"].unique())))

col3, col4 = st.columns(2)
with col3:
    et = st.selectbox("Employment Type",["Select Type"] + list(sample_csv["Employment.Type"].unique()))
with col4:
    er = st.selectbox("Education", ["Select Education"] + list(sample_csv["Education.Required"].unique()))

try:
    if st.button("Search Jobs", use_container_width = True):
        inp_pos = correct_type(pos).lower()
        inp_sta = sta.replace(" ", "").lower()
        inp_ci = ci.replace(" ", "").lower()
        inp_et = correct_type(et).lower()
        inp_er = er.replace(" ", "").lower()

        rec_jobs, rec_company, rec_city, rec_state = recommend(inp_pos)

        rec_data = {"Jobs" : rec_jobs, "Company" : rec_company, "City" : rec_city, "State" : rec_state}
        rec_df = pd.DataFrame(rec_data)
        rec_df.index = rec_df.index + 1

        st.table(rec_df)
except:
    st.error("Please select Job Title")