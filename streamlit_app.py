import streamlit as st
from langgraph.graph import StateGraph, END
from genai_config import configure_gemini
from prompt_generator import generate_prompt
import re
from Agents import MainAgent

agent = MainAgent()
def display_header():
    """Displays the header with the logo."""
    try:
        # Load the image from the specified path
        from PIL import Image
        image = Image.open("configs/OrangeLogo.jpg")

        st.markdown(
            f"""
            <div style="display: flex; align-items: center; background-color: black; padding: 10px;">
                <img src="data:image/png;base64,{image_to_base64(image)}" width="150" style="margin-right: 20px;">
                <h1 style="color: white; margin-top: 0px; margin-bottom: 0px;">AI Marketing Strategy Generator</h1>
            </div>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.error("Error: OrangeLogo.jpg not found in the configs directory.")
    except Exception as e:
        st.error(f"Error displaying header: {e}")

# Helper function to convert image to base64
import base64
def image_to_base64(image):
    """Converts a PIL image to base64 encoding for embedding in HTML."""
    import io
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str
# Custom CSS styling
def project():
    st.markdown("""
    <style>
        /* Black top rectangle */
        .top-rectangle {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 60px;
            background-color: #000000;
            z-index: 999;
        }
        
        /* Main content adjustment */
        .main > div {
            margin-top: 70px !important;
        }
        
        /* Button hover effects */
        .stButton button {
            background-color: #2a3f5f;
            color: orange;
            transition: all 0.3s ease;
            border: none;
        }
        
        /* Dropdown hover effects */
        .stSelectbox:hover select {
            border-color: #FF4B00 !important;
        }

        .stSelectbox select:focus {
            border-color: #FF4B00 !important;
            box-shadow: 0 0 0 0.2rem rgba(255, 75, 0, 0.25) !important;
        }

        /* Strategy output styling */
        .strategy-section {
            background: #fff;
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .strategy-section h3 {
            color: #FF4B00 !important;
            border-bottom: 2px solid #FF4B00;
            padding-bottom: 10px;
            margin-top: 0 !important;
        }

        .strategy-output ul {
            padding-left: 25px;
        }

        .strategy-output li {
            margin-bottom: 10px;
            line-height: 1.6;
        }    
        
        .stForm {background-color: #f9f9f9; padding: 20px; border-radius: 10px;}
        h1 {color: #2a3f5f;}
        .stTextArea textarea {min-height: 150px;}
        .metric-container {background: white!important; border-radius: 10px; padding: 15px;}
        .stSelectbox, .stTextInput, .stNumberInput {margin-bottom: 15px;}
    </style>
    """, unsafe_allow_html=True)

    # Add black rectangle at the top
    st.markdown('<div class="top-rectangle"></div>', unsafe_allow_html=True)

    campaign_workflow = agent.graph

    # Streamlit UI Components
    with st.form("strategy_form"):
        cols = st.columns(2)
        
        with cols[0]:
            business_idea = st.text_area("💡 Business Idea Description", 
                                    placeholder="Describe your business, product/service, and unique value proposition...")
            theme = st.selectbox("🎯 Campaign Theme", 
                            ["Brand Launch", "Product Expansion", "Seasonal Promotion", 
                                "Customer Retention", "Crisis Recovery", "Market Dominance"])
            product = st.text_input("📦 Product/Service Name", placeholder="Official product/service name")
            
        with cols[1]:
            goal = st.selectbox("🎯 Primary Objective", 
                            ["Market Penetration", "Lead Generation", "Brand Awareness", 
                            "Customer Acquisition", "Sales Boost", "Community Building"])
            budget = st.selectbox("💰 Budget Range", 
                                ["$1k-$5k", "$5k-$15k", "$15k-$50k", "$50k-$100k", "$100k+"])

            segment = st.selectbox("🎯 Target Audience", 
                                ["Loyal High-Income Customers", 
                                "Engaged Budget Shoppers", 
                                "Young High-Spending Consumers"])
            
        st.divider()
        
        with st.container():
            subcols = st.columns(2)
            with subcols[0]:
                growth_channel = st.selectbox("📈 Primary Growth Channel", 
                                            ["Social Media", "Search Ads", "Content Marketing", 
                                            "Influencer Partnerships", "Viral Marketing"])
            with subcols[1]:
                comms_channel = st.selectbox("📧 Communication Channel", 
                                        ["Email Marketing", "SMS Campaigns", "Push Notifications", 
                                            "Messenger Apps", "Webinars"])
        
        restrictions = st.text_input("🚫 Legal/Platform Restrictions", 
                                placeholder="List any compliance requirements or platform restrictions...")
        
        submitted = st.form_submit_button("✨ Generate Marketing Strategy", use_container_width=True)

    if submitted:
        campaign_state = {
            'business_idea': business_idea,
            'theme': theme,
            'product': product,
            'goal': goal,
            'budget': budget,
            'growth_channel': growth_channel,
            'comms_channel': comms_channel,
            'segment': 'A',
            'restrictions': restrictions,
            'trends_data' : "",
            'customer_data': "",
            'ideation_output': [],
            'detailed_content': [],
            "messages":[],
        }
        config = {"configurable":{"thread_id":1}}
        
        result = campaign_workflow.invoke(campaign_state,config=config)

        if 'error' in result:
            st.error(f"⚠️ Generation Error: {result['error']}")
        else:
            st.success("🎉 Strategy Generated Successfully!")
            st.divider()

            # Business Overview
            st.markdown("### 📌 Business Overview")
            cols = st.columns(2)
            with cols[0]:
                st.markdown(f"**Business Concept:**\n{business_idea}")
            with cols[1]:
                st.markdown(f"""
                <div class="metric-container">
                    <p>🏷️ Theme: <strong>{theme}</strong></p>
                    <p>🎯 Product: <strong>{product}</strong></p>
                    <p>💰 Budget: <strong>{budget}</strong></p>
                </div>
                """, unsafe_allow_html=True)

            # Budget Visualization
            st.markdown(result.get('detailed_content', ''))
            campaign_output = result.get('detailed_content', '')
            if '### 3. Budget Allocation' in campaign_output:
                try:
                    budget_section = campaign_output.split('### 3. Budget Allocation')[1].split('###')[0]
                    budget_items = [line.strip() for line in budget_section.split('\n') if line.startswith('-')]
                    
                    labels = []
                    sizes = []
                    for item in budget_items:
                        match = re.match(r'- (.*?): (\d+)%', item)
                        if match:
                            labels.append(match.group(1))
                            sizes.append(int(match.group(2)))

                except Exception as e:
                    st.warning("Could not generate budget visualization")

            # Structured Strategy Output
            st.markdown("### 📈 Comprehensive Marketing Strategy")
            st.markdown('<div class="strategy-output">', unsafe_allow_html=True)
            st.markdown(result.get('detailed_content', ''))
            st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Display the header
    display_header()
    project()
    # Call the strategy generator tab directl


if __name__ == "__main__":
    main()