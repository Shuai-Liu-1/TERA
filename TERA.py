import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import scipy.stats as stats

data= pd.read_csv("all.csv")
data["year"] = data["year"].astype(str)

# Set page configuration
#st.set_page_config(page_title="Teacher Evaluation Dashboard", layout="wide")

# Sidebar navigation
st.sidebar.title("TERA")
page = st.sidebar.radio("Go to", ["Data Prepare", "Data Analysis"])
########################################


if page == "Data Prepare":
    st.header("Data Prepare",divider=True)

    st.markdown("""
    ### 1. Data Cleaning  

    #####  Step 1: Standardizing Race/Ethnicity Codes  
    - Update the `reth` column in `tdemo2013.csv` to match the format used in `tdemo2014.csv` and `tdemo2015.csv`, where race is represented as:  
        - "White"  
        - "Black"  
        - "Hispanic"  
        - "Other"  
    - In `tdemo2013.csv`, the existing `reth` codes are:  
        - 1 → "White"  
        - 2 → "Black"  
        - 3 → "Hispanic"  
        - 4 → "Other"  
    - Modify `tdemo2013.csv` accordingly and save the updated file as `tdemo2013_reth.csv`.  

    ##### Step 2: Standardizing Gender Codes  
    - In `tdemo2014.csv`, the `female` column is encoded as:  
        - 1 → Male   
        - 2 → Female 
    - However, in `tdemo2013.csv` and `tdemo2015.csv`, the `female` column is coded as:  
        - 0 → Male  
        - 1 → Female  
    - To ensure consistency across all files, update `tdemo2014.csv` to use the `0,1` coding format.  
    - Save the updated file as `tdemo2014_female.csv`.  

    ##### Step 3: Editing District Names  
    - In `teval2015.csv`, the `districtname` column includes the word "District" (e.g., **"Radnor District"**).  
    - In `teval2013.csv` and `teval2014.csv`, district names do not contain the word "District" (e.g., **"Radnor"**).  
    - To maintain consistency, remove "District" from all values in the `districtname` column of `teval2015.csv`.  
    - Save the updated file as `teval2015_district.csv`.  
    ##### Step 4: Remove duplicate rows
                
    ### 2. Data Combination  

    #####  Step 1: Merge Evaluation Data
    - Combine `teval2013.csv`, `teval2014.csv`, and `teval2015_district.csv`.  
    - Save the merged dataset as `combined_teval.csv`.  

    #####  Step 2: Merge Demographic Data
    - Combine `tdemo2013_reth.csv`, `tdemo2014_female.csv`, and `tdemo2015.csv`.   
    - Save the merged dataset as `combined_tdemo.csv`.  

    #####  Step 3: Final Merge
    - Merge `combined_teval.csv` and `combined_tdemo.csv` on `"id"`, `"year"`, and `"districtname"`.  
    - Since `"districtno"` and `"districtname"` are duplicates, remove `"districtno"` from both files before merging.  
    - Save the final dataset as `all.csv`.  
    """)
    st.subheader("Data Quality Issues & Governance Suggestions", divider=True)

    st.markdown("""
    ##### **Data Quality Issues & Challenges**  

    1. **Duplicate Records:**  
    - Several datasets contain duplicate entries, leading to redundancy and potential inconsistencies in analysis.  
    - Merging files without addressing duplicates may result in inflated counts and incorrect statistical interpretations.  
    - It is essential to establish a robust deduplication process to ensure data accuracy.  

    2. **Inconsistent Identifiers:**  
    - The presence of both `"districtno"` and `"districtname"` creates ambiguity in district identification.  
    - Merging datasets without resolving this duplication may cause data mismatches.  
    - A standardized approach should be adopted to use a single, unique district identifier.  

    3. **File Structure Variability:**  
    - Datasets from different years and sources have structural inconsistencies, such as variations in column names, data types, and missing attributes.  
    - These inconsistencies require careful preprocessing to align schemas before data integration.  
    - A predefined data structure template should be enforced to maintain uniformity across datasets.  

    4. **Potential Missing Data:**  
    - Some records have incomplete or missing values, particularly when merging evaluation and demographic data.  
    - Missing data may lead to biased analysis and misinterpretations of trends.  
    - Imputation techniques or data validation rules should be implemented to handle gaps effectively.  

    ##### **Data Governance Recommendations**  

    1. **Standardized Data Format:**  
    - Define a consistent data format across all datasets to ensure compatibility during integration.  
    - Establish strict data entry protocols to minimize inconsistencies in future data collection.  

    2. **Duplicate Handling Policies:**  
    - Implement automated checks to detect and remove duplicate records while preserving necessary information.  
    - Maintain a log of deduplication steps to track data modifications.  

    3. **Unique Identifiers for Data Consistency:**  
    - Standardize district identification by using `"districtname"` as the primary key and removing redundant `"districtno"` fields.  
    - Ensure all records are consistently labeled across different datasets.  

     
    """)










######################
elif page == "Data Analysis":
    st.header("Data Analysis")
    st.subheader("Overall Distribution of Evaluation Scores",divider=True)
    fig_hist= px.histogram(data, y="eval", title="Distribution of Evaluation Scores",
                        orientation='h' )
    fig_hist.update_xaxes(title_text="Count") 
    fig_hist.update_yaxes(title_text="Evaluation") 

    pie_data = data['eval'].value_counts().reset_index()
    pie_data.columns = ['Evaluation', 'Count']
    fig_pie = px.pie(pie_data, names='Evaluation', values='Count', hole=0.3)
    col1, col2 = st.columns([3,1],gap="medium")
    with col1:
        st.plotly_chart(fig_hist)
    with col2:
        st.plotly_chart(fig_pie)

    st.markdown("""
    ###### **Evaluation Score Distribution**  

    - The most common evaluation score is **4**, accounting for **5,215** instances (**36.7%** of all records).  
    - The second most common score is **3**, with **4,408** instances (**31.1%** of all records).  
    """)

    ##################################################
    st.subheader("Evaluation Score Distribution by District",divider=True)

    color_map = {
        "Radnor": "darkorange",
        "Westlake": "darkred",
        "Kentwood": "darkgreen"
    }

    district_options = data["districtname"].unique()
    selected_district = st.selectbox("Please select a district to view the distribution of teacher evaluation scores below:", district_options)
    filtered_data = data[data["districtname"] == selected_district]

    hist_color = color_map.get(selected_district, "blue")
    fig_hist = px.histogram(filtered_data, y="eval", title=f"Evaluation Score Distribution in {selected_district} District",
                            labels={"eval": "Evaluation"}, 
                            color_discrete_sequence=[hist_color],orientation='h')
    fig_hist.update_xaxes(title_text="Count") 
    fig_hist.update_yaxes(title_text="Evaluation") 
    pie_data = filtered_data['eval'].value_counts().reset_index()
    pie_data.columns = ['Evaluation', 'Count']

    fig_pie = go.Figure(data=[go.Pie(labels=pie_data['Evaluation'], values=pie_data['Count'], hole=0.3)])
    fig_pie.update_layout()

    col1, col2 = st.columns([3,1],gap="medium")

    with col1:
        st.plotly_chart(fig_hist)

    with col2:
        st.plotly_chart(fig_pie)

    #average
    avg_eval_by_district = data.groupby("districtname")["eval"].mean().reset_index()
    district_fig = px.bar(avg_eval_by_district, x="districtname", y="eval", 
                        title="Average Evaluation Scores Across Districsts",
                        labels={"eval": "Average Evaluation Score"},
                        color="districtname",
                        text_auto='.3s',
                        color_discrete_map=color_map)  # Update y-axis label
    district_fig.update_yaxes(range=[avg_eval_by_district["eval"].min() -0.25, avg_eval_by_district["eval"].max() + 0.25])
    district_fig.update_xaxes(title_text="District") 
    st.plotly_chart(district_fig)

    ########################
    # average by distrct
    data['eval'] = pd.to_numeric(data['eval'], errors='coerce')
    avg_eval_by_year_district = data.groupby(["year", "districtname"])["eval"].mean().reset_index()

    # Create the bar chart
    year_district_fig = px.bar(
        avg_eval_by_year_district, 
        x="year", 
        y="eval", 
        color="districtname",  
        title="Average Evaluation Scores by Each Year Across Districts",
        labels={"eval": "Average Evaluation Score", "year": "Year", "districtname": "District"},
        barmode="group",
        text_auto='.3s',
        color_discrete_map=color_map
    )

    # Show the chart in Streamlit
    st.plotly_chart(year_district_fig)

    st.markdown("""
        ###### **Evaluation Score Trends by District**  

        - In both **Radnor** and **Kentwood** districts, the most common score is **4**, while in **Westlake**, the most common score is **3**.  
        - **Kentwood** has the highest overall average score (**3.74**), whereas **Westlake** has the lowest (**3.51**) over the three-year period.  
        - However, in **2015**, **Westlake** recorded the highest average score (**3.70**), while **Kentwood** had the lowest (**3.39**) among the three districts.  
        - **Kentwood's** average score declined from **2013 to 2015**, whereas **Westlake's** average score increased over the same period.  
        """)
    ########################################################
    color_map1 = {
        "2013": "steelblue",
        "2014": "deepskyblue",
        "2015": "dodgerblue"
    }
    st.subheader("Evaluation Scores Across Years",divider=True)


    fig_hist = px.histogram(filtered_data, y="eval", 
                            title=f"Overlaid Evaluation Score Distribution by Year",
                            labels={"eval": "Evaluation"}, 
                            color="year", 
                            orientation='h',
                            barmode='overlay',
                            color_discrete_map=color_map1)
    fig_hist.update_xaxes(title_text="Count") 
    fig_hist.update_yaxes(title_text="Evaluation") 
    st.plotly_chart(fig_hist)



    district_options = data["year"].unique()
    selected_year= st.selectbox("Please select a year to view the distribution of teacher evaluation scores below:", district_options)
    filtered_data = data[data["year"] == selected_year]
    hist_color = color_map1.get(selected_year, "blue")
    fig_hist = px.histogram(filtered_data, y="eval", 
            title=f"Evaluation Score Distribution in year {selected_year}",
                            labels={"eval": "Evaluation"}, 
                            color_discrete_sequence=[hist_color],
                            orientation='h')

    fig_hist.update_xaxes(title_text="Count") 
    fig_hist.update_yaxes(title_text="Evaluation") 

    pie_data = filtered_data['eval'].value_counts().reset_index()
    pie_data.columns = ['Evaluation', 'Count']

    fig_pie = go.Figure(data=[go.Pie(labels=pie_data['Evaluation'], 
                        values=pie_data['Count'], hole=0.3)])
    fig_pie.update_layout()
    col1, col2 = st.columns([3,1],gap="medium")
    with col1:
        st.plotly_chart(fig_hist)
    with col2:
        st.plotly_chart(fig_pie)


    #AVERAGE
    avg_eval_by_year = data.groupby("year")["eval"].mean().reset_index()
    year_fig = px.bar(avg_eval_by_year, x="year", y="eval", 
                    title="Average Evaluation Scores by Year",
                    color="year",        
                    text_auto='.3s',        
                    color_discrete_map=color_map1)
    year_fig.update_yaxes(range=[avg_eval_by_year["eval"].min() -0.25, avg_eval_by_district["eval"].max() + 0.25])
    year_fig.update_xaxes(title_text="Year",dtick=1) 
    year_fig.update_yaxes(title_text="Average Evaluation Score") 
    st.plotly_chart(year_fig)


    st.markdown("""
    ###### **Evaluation Score Trends by Year**  

    - **2013** recorded the highest number of **5** scores among the three years, with a total of **910** instances.  
    - **2013** also had the highest count of **4** scores, totaling **1,595**.  
    - **2014** saw the highest number of **2** scores, with a total of **595** instances.  
    - The highest average score occurred in **2013**, with an average of **3.79**.  
    - The lowest average score was observed in **2014**, with an average of **3.47**.  
    """)

    ########################################################

    color_map2 = {
        "Female": "lightpink",
        "Male": "lightblue",

    }

    st.subheader("Evaluation Scores by Gender",divider=True)
    data['female'] = data['female'].astype('category')
    #data['eval'] = data['eval'].astype('category')
    contingency_table = pd.crosstab(data['female'], data['eval'])
    n = contingency_table.sum().sum()  # Total number of observations
    min_dim = min(contingency_table.shape) - 1  # The minimum of the number of rows - 1 or columns - 1
    chi2, p, dof, expected = stats.chi2_contingency(contingency_table)
    # Calculate Cramer's V
    cramers_v = np.sqrt(chi2 / (n * min_dim))
    # Display the result
    st.write(f"Cramer's V between Gender and Evaluation: **{cramers_v:.4f}**")
    st.write('This suggests that a teacher’s gender does not significantly impact their evaluation scores based on this dataset.The relationship observed is likely due to random variation rather than a meaningful pattern.')
    data['gender_label'] = data['female'].map({1: 'Female', 0: 'Male'})

    fig_hist = px.histogram(data, y="eval", 
                            title=f"Overlaid Evaluation Score Distribution by Gender",
                            labels={"eval": "Evaluation","gender_label":"Gender"}, 
                            color="gender_label", 
                            orientation='h',
                            barmode='overlay',
                            color_discrete_map=color_map2)
    fig_hist.update_xaxes(title_text="Count") 
    fig_hist.update_yaxes(title_text="Evaluation") 

    #st.plotly_chart(fig_hist)

    pie_data = data['gender_label'].value_counts().reset_index()
    pie_data.columns = ['Gender', 'Count']
    fig_pie = px.pie(pie_data,  values='Count', hole=0.3, color="Gender",
                    color_discrete_map=color_map2)
    col1, col2 = st.columns([3,1],gap="medium")
    with col1:
        st.plotly_chart(fig_hist)
    with col2:
        st.plotly_chart(fig_pie)

    #AVERAGE
    avg_eval_by_gender = data.groupby("gender_label")["eval"].mean().reset_index()
    gender_fig = px.bar(avg_eval_by_gender, x="gender_label", y="eval", 
                    title="Average Evaluation Scores by Gender",
                    labels={"gender_label":"Gender"},
                    color="gender_label",  
                    text_auto='.3s',              
                    color_discrete_map=color_map2)
    gender_fig.update_yaxes(range=[avg_eval_by_gender["eval"].min() -0.25, avg_eval_by_gender["eval"].max() + 0.25])
    #gender_fig.update_xaxes(title_text="Year",dtick=1) 
    gender_fig.update_yaxes(title_text="Average Evaluation Score") 
    st.plotly_chart(gender_fig)


    #data['eval'] = pd.to_numeric(data['eval'], errors='coerce')
    avg_eval_by_year_gender = data.groupby(["year", "gender_label"])["eval"].mean().reset_index()

    # Create the bar chart
    year_district_fig = px.bar(
        avg_eval_by_year_gender, 
        x="year", 
        y="eval", 
        color="gender_label",  
        title="Average Evaluation Scores by Gender in Three years",
        labels={"eval": "Average Evaluation Score", "year": "Year", "gender_label": "Gender"},
        barmode="group",
        text_auto='.3s',
        color_discrete_map=color_map2
    )
    year_district_fig.update_yaxes(range=[avg_eval_by_year_gender["eval"].min() -0.25, avg_eval_by_year_gender["eval"].max() + 0.25])

    # Show the chart in Streamlit
    st.plotly_chart(year_district_fig)

    #st.dataframe(avg_eval_by_year_gender)
    st.markdown("""
    ###### **Evaluation Scores by Gender**  

    - The number of **female** participants(contain repeat) is higher than that of **male** participants, with **11,680** females (representing **79.6%**) and **2,292** males (representing **20.4%**).  
    - There is very little difference in the average scores between genders, with females having an average score of **3.59** and males having an average score of **3.60**.  
    """)



    ########################################################
    color_map3 = {
        "White": px.colors.qualitative.Safe[0],
        "Black": px.colors.qualitative.Alphabet[11],
        "Hispanic":px.colors.qualitative.Plotly[2],
        "Other":px.colors.qualitative.Plotly[0]
    }

    st.subheader("Evaluation Scores by Race",divider=True)
    data['eval'] = data['eval'].astype('category')
    contingency_table = pd.crosstab(data['reth'], data['eval'])
    n = contingency_table.sum().sum()  # Total number of observations
    min_dim = min(contingency_table.shape) - 1  # The minimum of the number of rows - 1 or columns - 1
    chi2, p, dof, expected = stats.chi2_contingency(contingency_table)
    # Calculate Cramer's V
    cramers_v = np.sqrt(chi2 / (n * min_dim))
    # Display the result
    st.write(f"Cramer's V between Race and Evaluation: **{cramers_v:.4f}**")
    st.write('There is no strong evidence that race/ethnicity is a significant factor in teacher evaluations based on the data. However, Small sample size in some racial groups could affect the statistical significance of the relationship.')


    fig_hist = px.histogram(data, y="eval", 
                            title=f"Overlaid Evaluation Score Distribution by Race",
                            labels={"eval": "Evaluation"}, 
                            color="reth", 
                            orientation='h',
                            barmode='overlay',
                            color_discrete_map=color_map3)
    fig_hist.update_xaxes(title_text="Count") 
    fig_hist.update_yaxes(title_text="Evaluation") 
    #st.plotly_chart(fig_hist)
    pie_data = data['reth'].value_counts().reset_index()
    pie_data.columns = ['Race', 'Count']
    fig_pie = px.pie(pie_data,  values='Count', hole=0.3, color="Race",
                    color_discrete_map=color_map3)
    col1, col2 = st.columns([3,1],gap="medium")
    with col1:
        st.plotly_chart(fig_hist)
    with col2:
        st.plotly_chart(fig_pie)

    data['eval'] = pd.to_numeric(data['eval'], errors='coerce')
    avg_eval_by_race = data.groupby("reth")["eval"].mean().reset_index()
    custom_order = ["White", "Black", "Hispanic", "Other"]
    race_fig = px.bar(avg_eval_by_race, x="reth", y="eval", 
                    title="Average Evaluation Scores by Race",
                    labels={"race":"Race"},
                    category_orders={"reth": custom_order},
                    color="reth",           
                    text_auto='.3s',     
                    color_discrete_map=color_map3)
    race_fig.update_yaxes(range=[avg_eval_by_race["eval"].min() -0.25, avg_eval_by_race["eval"].max() + 0.25])
    race_fig.update_yaxes(title_text="Average Evaluation Score") 
    st.plotly_chart(race_fig)
    #st.dataframe(avg_eval_by_race)


    avg_eval_by_year_race = data.groupby(["year", "reth"])["eval"].mean().reset_index()

    # Create the bar chart
    race_fig = px.bar(
        avg_eval_by_year_race, 
        x="year", 
        y="eval", 
        color="reth",  
        title="Average Evaluation Scores by Race in Three years",
        labels={"eval": "Average Evaluation Score", "year": "Year", "reth": "Race"},
        barmode="group",
        text_auto='.3s',
        color_discrete_map=color_map3
    )
    race_fig.update_yaxes(range=[avg_eval_by_year_race["eval"].min() -0.25, avg_eval_by_year_race["eval"].max() + 0.25])

    # Show the chart in Streamlit
    st.plotly_chart(race_fig)
    #st.dataframe(avg_eval_by_year_race)

    st.markdown("""
    ###### **Evaluation Scores by Race**  

    - **White** teachers represent **88.5%** of the total, with **12,777** instances.  
    - The second-largest group is **Black**, comprising **7.29%** of the total, with **1,053** instances.  
    - **Other** races have the highest average score of **3.71**, followed by **Hispanic** students with an average score of **3.68**.  
    """)


    ###########################
    #by district by gender
    st.subheader("Evaluation Scores by distrct by gender",divider=True)
    district_options = data['districtname'].unique()
    race_options = ['White','Black','Hispanic',"Other"]
    col1, col2 = st.columns([1,1],gap="medium")
    with col1:
        selected_district = st.selectbox("Select District", district_options)
    with col2:
        selected_race = st.selectbox("Select Race", race_options)

    filtered_data = data[data['districtname'] == selected_district]
    filtered_data2=filtered_data[filtered_data['reth']==selected_race]
    filtered_data2['gender_label'] = filtered_data2['female'].map({1: 'Female', 0: 'Male'})

    # Create the histogram
    fig_hist = px.histogram(
        filtered_data2, 
        y="eval", 
        title=f"Overlaid Evaluation Score Distribution by Gender in {selected_district}",
        labels={"eval": "Evaluation", "gender_label": "Gender"}, 
        color="gender_label", 
        orientation='h',  # Horizontal orientation
        barmode='overlay',  # Overlaid bars
        color_discrete_map=color_map1  
    )

    fig_hist.update_xaxes(title_text="Count") 
    fig_hist.update_yaxes(title_text="Evaluation")
    #st.plotly_chart(fig_hist)




    data['eval'] = pd.to_numeric(data['eval'], errors='coerce')
    avg_eval_by_district_by_year = data.groupby(["districtname", "reth","year"])["eval"].mean().reset_index()

    filtered_avg = avg_eval_by_district_by_year[avg_eval_by_district_by_year["districtname"] == selected_district]
    filtered_avg2 = filtered_avg [filtered_avg ["reth"] == selected_race]

    year_fig = px.bar(
        filtered_avg2, 
        x="year", 
        y="eval", 
        title=f"Average Evaluation Scores by Year in {selected_district} with {selected_race}",
        color="year",                
        text_auto='.3s',
        color_discrete_map=color_map1
    )
    year_fig.update_yaxes(range=[avg_eval_by_district_by_year["eval"].min() -0.25, avg_eval_by_district_by_year["eval"].max() + 0.25])
    year_fig.update_xaxes(title_text="Year",dtick=1) 
    year_fig.update_yaxes(title_text="Average Evaluation Score")
    #st.plotly_chart(year_fig) 

    col1, col2 = st.columns([1,1],gap="medium")
    with col1:
        st.plotly_chart(fig_hist)
    with col2:
        st.plotly_chart(year_fig)

    st.markdown("""
    ###### **Evaluation Scores of White Teachers by District and Year**  

    **1. Radnor District**:  
    - Highest average score: **3.76** (2013)  
    - Lowest average score: **3.44** (2014)  

    **2. Kentwood District**:  
    - Highest average score: **4.43** (2013)  
    - Lowest average score: **3.39** (2015)  

    **3. Westlake District**:  
    - Highest average score: **3.78** (2015)  
    - Lowest average score: **3.12** (2013)  
    """)

    #st.dataframe(avg_eval_by_district_by_year)
