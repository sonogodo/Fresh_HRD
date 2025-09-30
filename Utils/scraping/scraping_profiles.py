import json
import time
import requests
from linkdapi import LinkdAPI

def profile_scraping(linkedin_data):
  '''
  Extract profile information from Linkedin using data from recent graduate
  '''
  # Fetch profile data using LinkdAPI
  api_key = "'li-x9iGcadaE8qUFPq0-i5rzanqXpqSi2PKuLzwW_T0qn0iFki_xwpgBq_HVDb-fUedfZNk_2s7nwWkEKyLHfyX-f3OdIVhdA'"
  headers = {"X-linkdapi-apikey": f"{api_key}"}

  all_profiles_data = []
  not_found_profile = []
  
  file_path = '/linkedin_success_master.json'
  try:
    with open(file_path, 'r') as f:
      linkedin_data = json.load(f)
  except FileNotFoundError:
    print(f"Error: The file {file_path} was not found.")
  except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from the file {file_path}.")
  except Exception as e:
    print(f"An error occurred: {e}")

  linkedin_urls = [item.get('LinkedIn URL') for item in linkedin_data if item.get('LinkedIn URL')]
  linkedin_ids = [url.split('/in/')[-1].split('/')[0] for url in linkedin_urls]

  if linkedin_ids: # Only proceed if LinkedIn IDs were extracted
    for profile_id in linkedin_ids:
      combined_data = {}
      # profile overview
      url_ov = f"https://linkdapi.com/api/v1/profile/overview?username={profile_id}"
      overview_response = requests.get(url_ov, headers=headers)
      
      if overview_response.status_code == 200:
        overview_data = overview_response.json()
        if overview_data and overview_data.get('success'):
          combined_data.update(overview_data.get('data', {}))
          urn = overview_data.get('data', {}).get('urn')
          full_name = overview_data.get('data', {}).get('fullName', 'N/A') # Get full name here
          if urn:
            # profile skills
            url_skills = f"https://linkdapi.com/api/v1/profile/skills?urn={urn}"
            skills_response = requests.get(url_skills, headers=headers)
            if skills_response.status_code == 200:
              skills_data = skills_response.json()
              if skills_data and skills_data.get('success'):
                combined_data['skills'] = skills_data.get('data', {}).get('skills', [])
            # profile certifications
            url_cert = f"https://linkdapi.com/api/v1/profile/certifications?urn={urn}"
            certifications_response = requests.get(url_cert, headers=headers)
            if certifications_response.status_code == 200:
              certifications_data = certifications_response.json()
              if certifications_data and certifications_data.get('success'):
                combined_data['certifications'] = certifications_data.get('data', {}).get('certifications', [])
            # profile education
                url_educ = f"https://linkdapi.com/api/v1/profile/education?urn={urn}"
                education_response = requests.get(url_educ, headers=headers)
                if education_response.status_code == 200:
                  education_data = education_response.json()
                  if education_data and education_data.get('success'):
                    combined_data['education'] = education_data.get('data', {}).get('education', [])
      else:
        not_found_profile.append(profile_id)
        print(f"Error fetching overview for {profile_id}: Status Code {overview_response.status_code}")
        
      all_profiles_data.append(combined_data)
      time.sleep(20) # Add a small delay to avoid hitting the rate limit
      
  # Transform the collected data
  transformed_data = []

  for profile in all_profiles_data:
    profile_id = profile.get('fullName', 'N/A')  # Use 'fullName' as the ID
    summary = profile.get('summary', '') # Get summary here
    link = profile.get('publicIdentifier', '')
    skills = profile.get('skills', [])
    education = profile.get('education', [])
    certifications = profile.get('certifications', []) # Include certifications as well
    
    # Concatenate summary, skills, education, and certifications into a single string for 'perfil'
    perfil_string = ""
    if summary:
      perfil_string += "Summary: " + summary + ". "
    if link:
      link_string = "https://br.linkedin.com/in/"+link
    if skills:
      perfil_string += "Skills: " + ", ".join([skill.get('skillName', '') for skill in skills]) + ". "
    if education:
      education_details = []
      for edu in education:
        edu_string = f"{edu.get('degree', '')} at {edu.get('university', '')}"
        education_details.append(edu_string)
        perfil_string += "Education: " + "; ".join(education_details) + ". "
    if certifications:
      certification_details = []
      for cert in certifications:
        cert_string = f"{cert.get('certificationName', '')}"
        certification_details.append(cert_string)
        perfil_string += "Certifications: " + "; ".join(certification_details) + "."
        
    transformed_data.append({
      "id": profile_id,
      "perfil": perfil_string.strip(),
      "link": link_string
    })

  normalized_data = []
  
  def normalize_characters(text):
    """Converts special characters to their normal equivalents."""
    text = text.replace('ç', 'c').replace('Ç', 'C')
    text = text.replace('ã', 'a').replace('Ã', 'A')
    text = text.replace('á', 'a').replace('Á', 'A')
    text = text.replace('à', 'a').replace('À', 'A')
    text = text.replace('é', 'e').replace('É', 'E')
    text = text.replace('ê', 'e').replace('Ê', 'E')
    text = text.replace('í', 'i').replace('Í', 'I')
    text = text.replace('ó', 'o').replace('Ó', 'O')
    text = text.replace('ô', 'o').replace('Ô', 'O')
    text = text.replace('ú', 'u').replace('Ú', 'U')
    text = text.replace('ü', 'u').replace('Ü', 'U')
    text = text.replace('ñ', 'n').replace('Ñ', 'N')
    # Add more replacements as needed
    return text
  
  for item in transformed_data:
    normalized_perfil = normalize_characters(item.get('perfil', ''))
    normalized_data.append({
      "id": item.get('id', 'N/A'),
      "perfil": normalized_perfil,
      "link": item.get('link', '')
    })
    
  # Print the normalized data as a JSON string
  normalized_json = json.dumps(normalized_data, indent=4, ensure_ascii=False)

  output_normalized_file_path = 'likedin_profiles.json'
  with open(output_normalized_file_path, 'w', encoding='utf-8') as f:
    f.write(normalized_json)
  return normalized_json
