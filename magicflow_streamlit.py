import streamlit as st
import requests
import json
import time

def get_output_url(country, qr_url_content):
    # First API call
    url1 = "https://api.magicflow.ai/workflow/a9551b0f-b36f-4ce6-a699-3821dfe6c2e6/job"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Token 670eJ5xit6Ptxf/pWoxrUeZtU1GPKolO/2XfZMecr26iNZ63PlVFCd6sbPy+4++o"
    }
    data = {
        "mock": False,
        "params": {
            "country": country,
            "qr-url-content": qr_url_content,
        }
    }
    response1 = requests.post(url1, headers=headers, data=json.dumps(data))
    response1_data = response1.json()

    # If need to display first response with JobId
    # st.write('First response:')
    # st.write(response1_data)

    # Assuming the job id is contained in the 'jobId' field of the response
    job_id = response1_data.get('jobId')

    # Initialize output_url to None
    output_url = None

    # Poll the server for up to 200 seconds
    for _ in range(100):

        # Second API call
        url2 = f"https://api.magicflow.ai/workflow/a9551b0f-b36f-4ce6-a699-3821dfe6c2e6/jobs/{job_id}/results"
        response2 = requests.get(url2, headers=headers)
        response2_data = response2.json()
        
        # If need to display second response with JobId, status, results
        # st.write('Second response:')
        # st.write(response2_data)

        # Try to get the output url from the result
        # output_url = response2_data.get('output')

        # Try to get the output url from the result
        results = response2_data.get('results')
        if results is not None:
            output_url = results.get('generate-qr')
    
        # If we got an output url, break the loop
        if output_url is not None:
            break

        # Wait for 1 second before the next attempt
        time.sleep(1)

    return output_url

def main():
    st.title('My Streamlit QR Code Generator App')

    # Text input for country
    country = st.text_input('Enter country')

    # Text input for QR URL content
    qr_url_content = st.text_input('Enter QR URL content')

    # Check if country and qr_url_content have been entered
    if country and qr_url_content:
        # Call the function to get output URL
        output_url = get_output_url(country, qr_url_content)

        st.write(f"The output URL is: {output_url}")

        # Display the image from the URL
        if output_url is not None:
            st.image(output_url)

if __name__ == "__main__":
    main()
