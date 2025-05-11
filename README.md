#  AI-Powered Marketing Campaign Generator
### Demo:
<a href="http://www.youtube.com/watch?feature=player_embedded&v=fIGaUP056WA"><img src="http://img.youtube.com/vi/fIGaUP056WA/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="1080" height="720" /></a>


##  Project Overview
The **AI-Powered Marketing Campaign Generator** is an innovative tool designed to assist marketers in a telecom company by leveraging **Large Language Models (LLMs)** to generate personalized and data-driven marketing campaigns. By providing key inputs such as customer segment, budget, campaign theme, and legal restrictions, this tool automates and enhances the campaign ideation process, ensuring efficient and impactful marketing strategies.

##  Key Features
- **AI-Driven Campaign Generation**: Generates customized marketing campaigns based on user inputs.
- **Customer-Centric Recommendations**: Tailors suggestions based on customer segmentation and market trends.
- **Multi-Channel Strategy**: Supports multiple communication and growth channels.
- **Legal Compliance Considerations**: Ensures campaigns adhere to platform-specific legal restrictions.
- **Insightful Data Analysis**: Uses customer data and trends to suggest the most effective strategies.

## 🛠 Installation & Setup
To set up and run the project, follow these steps:
### Option 1: Running Locally:
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/marketing-campaign-ai.git
   cd marketing-campaign-ai
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
### **Option 2: Running with Docker:**
1. Build the Docker Image
```bash
docker build -t my-streamlit-app
```
2. Run the container:
```bash
docker run -p 8501:8501 my-streamlit-app
```
## 🔄 How It Works
1. **User Input**: The marketer provides details such as customer segment, budget, business objective, campaign theme, and preferred communication channels.
2. **AI Processing**: The LLM analyzes the provided information and generates marketing campaign ideas.
3. **Content Evaluation**: A review module assesses the AI-generated content for relevance and quality.
4. **Final Output**: The tool presents a structured marketing campaign, ready for deployment or further refinement.

## 🔍 Assumptions
- We assumed that customers are already segmented, and the marketer will input the target audience (customer segment). This segmentation was created using collected data for digital marketing analysis ([https://drive.google.com/drive/folders/1vguKu-j89cHYBAarNUGEBWo_IDnaXz06?usp=sharing]).
- A simple customer segmentation was performed on this dataset using clustering since the data did not include predefined customer segments.
- We assumed that our generated clusters represent the customer segments that marketers will input.

### 📊 Dataset Description
 #### Overview:
This dataset provides a comprehensive view of customer interactions with digital marketing campaigns. It includes demographic data, marketing-specific metrics, customer engagement indicators, and historical purchase data, making it suitable for predictive modeling and analytics in the digital marketing domain.
 #### Features:
 ([https://www.kaggle.com/datasets/rabieelkharoua/predict-conversion-in-digital-marketing-dataset/data])
 #### 📉 Clustering Results:
 - The customers were segmented into 3 clusters and have these characteristics:
   - **Cluster 0:**
      - Age: ~40 years (middle-aged)
      - Income: ~$49,756 (lower-income group)
      - Ad Spend: ~$4,985 (moderate)
      - Click-Through Rate: ~15.4%
      - Conversion Rate: ~10.3%
      - Loyalty Points: ~2,498 (average)
      - Higher Website Visits (24.7) and Pages Per Visit (5.56)
      - High Engagement (Email Opens & Clicks)
      - Proposed Name: "Engaged Budget Shoppers"
   - **Cluster 1:**
      - Age: ~58 years (older demographic)
      - Income: ~$104,869 (higher-income group)
      - Ad Spend: ~$4,977 (similar to Cluster 0)
      - Click-Through Rate: ~15.4%
      - Conversion Rate: ~10.7% (slightly higher)
      - Loyalty Points: ~2,504 (slightly higher)
      - Higher Retention (Lower Previous Purchases but More Loyal)
      - Proposed Name: "Loyal High-Income Customers"
   - **Cluster 2:**
      - Age: ~35 years (youngest group)
      - Income: ~$116,438 (highest-income group)
      - Ad Spend: ~$5,043 (highest)
      - Click-Through Rate: ~15.6% (slightly higher)
      - Conversion Rate: ~10.3%
      - Loyalty Points: ~2,465 (slightly lower)
      - Most Tech-Savvy & Digital-Focused
      - Proposed Name: "Young High-Spending Consumers"

