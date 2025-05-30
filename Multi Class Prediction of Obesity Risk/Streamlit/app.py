import streamlit as st
import requests
import pandas as pd

# Define the FastAPI endpoint
url = "http://20.253.116.228/predict"

# Style for the result
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to translate prediction to human-readable form
def interpret_prediction(prediction):
    if prediction == 0:
        return "Insuffient Weight"
    elif prediction == 1:
        return "Healthy Weight"
    elif prediction == 2:
        return "Overweight Level 1"
    elif prediction == 3:
        return "Overweight Level 2"
    elif prediction == 4:
        return "Obesity Level 1"
    elif prediction == 5:
        return "Obesity Level 2"
    elif prediction == 6:
        return "Obesity Level 3"
    else:
        return "Unknown Level"
    

def main():
    st.title("Obesity Level Prediction")

    # User can choose to input data via form or upload CSV
    input_method = st.radio("How would you like to input data?", ('Fill Form', 'Upload CSV'))

    if input_method == 'Fill Form':
         # Initialize form fields with default values
        form_data = {
            "id": 0,
            "Gender": 'Male',
            "Age": 25.0,
            "Height": 1.75,
            "Weight": 70.0,
            "family_history_with_overweight": 'yes',
            "FAVC": 'yes',
            "FCVC": 2.0,
            "NCP": 3.0,
            "CAEC": 'Sometimes',
            "SMOKE": 'no',
            "CH2O": 2.0,
            "SCC": 'no',
            "FAF": 1.0,
            "TUE": 2.0,
            "CALC": 'Sometimes',
            "MTRANS": 'Public_Transportation'
        }

        # Create form to input data or display data from CSV
        with st.form(key='my_form'):
            id_field = st.number_input('ID', value=form_data["id"])
            gender = st.selectbox('Gender', ['Male', 'Female'], index=['Male', 'Female'].index(form_data["Gender"]))
            age = st.number_input('Age', min_value=18.00, max_value=100.00, value=form_data["Age"])
            height = st.number_input('Height (meters)', value=form_data["Height"])
            weight = st.number_input('Weight (kg)', value=form_data["Weight"])
            family_history_with_overweight = st.selectbox('Family history of overweight', ['yes', 'no'], index=['yes', 'no'].index(form_data["family_history_with_overweight"]))
            favc = st.selectbox('Frequent consumption of high caloric food', ['yes', 'no'], index=['yes', 'no'].index(form_data["FAVC"]))
            fcvc = st.number_input('Frequency of vegetables consumption', min_value=1.00, max_value=3.00, value=form_data["FCVC"])
            ncp = st.number_input('Number of main meals', value=form_data["NCP"])
            caec = st.selectbox('Consumption of food between meals', ['no', 'Sometimes', 'Frequently', 'Always'], index=['no', 'Sometimes', 'Frequently', 'Always'].index(form_data["CAEC"]))
            smoke = st.selectbox('Smoking', ['yes', 'no'], index=['yes', 'no'].index(form_data["SMOKE"]))
            ch2o = st.number_input('Consumption of water daily (liters)', value=form_data["CH2O"])
            scc = st.selectbox('Calories consumption monitoring', ['yes', 'no'], index=['yes', 'no'].index(form_data["SCC"]))
            faf = st.number_input('Physical activity frequency (times per week)', value=form_data["FAF"])
            tue = st.number_input('Time using electronic devices (hours per day)', value=form_data["TUE"])
            calc = st.selectbox('Consumption of alcohol', ['no', 'Sometimes', 'Frequently'], index=['no', 'Sometimes', 'Frequently'].index(form_data["CALC"]))
            mtrans = st.selectbox('Transportation used', ['Automobile', 'Motorbike', 'Bike', 'Public_Transportation', 'Walking'], index=['Automobile', 'Motorbike', 'Bike', 'Public_Transportation', 'Walking'].index(form_data["MTRANS"]))
            submit_button = st.form_submit_button(label='Predict Obesity Level')

            # Handle form submission
        if submit_button:
            # Construct the request payload
            data = {
                "id": id_field,
                "Gender": gender,
                "Age": age,
                "Height": height,
                "Weight": weight,
                "family_history_with_overweight": family_history_with_overweight,
                "FAVC": favc,
                "FCVC": fcvc,
                "NCP": ncp,
                "CAEC": caec,
                "SMOKE": smoke,
                "CH2O": ch2o,
                "SCC": scc,
                "FAF": faf,
                "TUE": tue,
                "CALC": calc,
                "MTRANS": mtrans
            }

        # Send a post request to the server
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            # Interpret the prediction for the user
            prediction = interpret_prediction(result.get('prediction', -1))
            # Display the prediction result
            st.markdown(f'<p class="big-font">Obesity Level: {prediction}</p>', unsafe_allow_html=True)
        else:
            st.error("Failed to get a valid response from the model.")

    elif input_method == 'Upload CSV':
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            dataframe = pd.read_csv(uploaded_file)
            # Create a new column for predictions in the dataframe
            dataframe['Obesity Level'] = None
            
            # Iterate over the rows of the dataframe and make predictions
            with st.spinner('Making predictions...'):
                for index, row in dataframe.iterrows():
                    # Convert the row to dictionary
                    data = row.to_dict()
                    print(data)
                    # Remove the 'Obesity Level' key if present
                    data.pop('Obesity Level', None)
                    # Send a post request to the server
                    response = requests.post(url, json=data)
                    if response.status_code == 200:
                        result = response.json()
                        # Interpret the prediction for the user
                        prediction = interpret_prediction(result.get('prediction', -1))
                        # Update the dataframe with predictions
                        dataframe.at[index, 'Obesity Level'] = prediction
                    else:
                        st.error(f"Failed to get a valid response from the model for row {index+1}: {response.text}")
                        break  # Stop the loop if there is an error

            # Only proceed if all predictions were successful
            if not dataframe['Obesity Level'].isnull().any():
                st.success('All predictions made successfully!')
                # Display the dataframe with predictions
                st.dataframe(dataframe)
                # Allow the user to download the augmented CSV
                st.download_button(
                    label="Download CSV with predictions",
                    data=dataframe.to_csv(index=False),
                    file_name='predictions.csv',
                    mime='text/csv'
                )
            else:
                st.error(f"Failed to get a valid response from the model: {response.text}")

if __name__ == "__main__":
    main()


        






