def generate_prompt(state):
    """Generates the marketing strategy prompt based on user inputs"""
    base_prompt = f"""
    Create a comprehensive marketing strategy for a business described as: 
    {state['business_idea']}

    Campaign Theme: {state['theme']}

    Target Product/Service: {state['product']}
    Primary Goal: {state['goal']}
    Budget Range: {state['budget']}
    Key Channels: {state['growth_channel']} (growth), {state['comms_channel']} (communication)
    Target Audience: {state['segment']}
    Restrictions: {state['restrictions'] or 'None'}

    Present the strategy using markdown formatting with the following sections:

    ### 1. Channel-Specific Execution Plan
    - Detailed tactics for {state['growth_channel']}
    - Integration with {state['comms_channel']}
    - Platform-specific recommendations

    ### 2. Content Strategy
    - Theme alignment: {state['theme']}
    - Content calendar overview
    - Key messaging pillars

    ### 3. Budget Allocation
    - Percentage breakdown across channels
    - Example: "Social Media (40%): ${state['budget']} allocation details"
    - Contingency fund allocation

    ### 4. 60-Day Execution Timeline
    - Phase 1: Launch Preparation (Days 1-15)
    - Phase 2: Soft Launch (Days 16-30)
    - Phase 3: Full Execution (Days 31-60)

    ### 5. Success Metrics
    - Primary KPIs for {state['goal']}
    - Weekly tracking methodology
    - Conversion funnel targets

    ### 6. Risk Mitigation
    - {state['restrictions'] or 'Standard'} compliance measures
    - Crisis response protocol
    - Performance recovery strategies
    """
    state['base_prompt'] = base_prompt
    return state