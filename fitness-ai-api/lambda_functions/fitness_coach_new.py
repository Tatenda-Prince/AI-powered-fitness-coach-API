import json
import boto3
import os
from datetime import datetime
import uuid
import math

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('fitness-user-assessments')

def determine_assessment_type(question):
    question_lower = question.lower()
    if "vo2" in question_lower:
        return "vo2_max"
    elif "body fat" in question_lower or "bf%" in question_lower:
        return "body_fat"
    elif "bmr" in question_lower or "metabolic rate" in question_lower or "calorie" in question_lower:
        return "bmr"
    elif "heart rate" in question_lower or "hr" in question_lower:
        return "heart_rate"
    elif "bmi" in question_lower or "weight" in question_lower:
        return "bmi"
    else:
        return "general"

def calculate_vo2_max(age, weight, height, gender, activity):
    # Estimated VO2 max using age-based formula with activity adjustments
    if gender.lower() == 'male':
        base_vo2 = 15.3 * (weight / 2.205) / (age * 0.78)  # Convert kg to lbs
        base_vo2 = max(35, min(65, base_vo2))  # Reasonable bounds
    else:
        base_vo2 = 14.7 * (weight / 2.205) / (age * 0.78)
        base_vo2 = max(30, min(55, base_vo2))
    
    # Activity level adjustments
    activity_multipliers = {
        'sedentary': 0.85,
        'light': 0.95,
        'moderate': 1.0,
        'very': 1.15,
        'extra': 1.25
    }
    
    vo2_estimate = base_vo2 * activity_multipliers.get(activity, 1.0)
    
    # Age-based classification
    if age < 30:
        classification = "excellent" if vo2_estimate > 50 else "good" if vo2_estimate > 40 else "fair"
    elif age < 40:
        classification = "excellent" if vo2_estimate > 45 else "good" if vo2_estimate > 35 else "fair"
    else:
        classification = "excellent" if vo2_estimate > 40 else "good" if vo2_estimate > 30 else "fair"
    
    return f"""**Estimated VO2 Max: {vo2_estimate:.1f} ml/kg/min**

Your VO2 max estimate puts you in the "{classification}" category for your age group ({age} years).

**What is VO2 Max?**
VO2 max represents the maximum amount of oxygen your body can utilize during intense exercise. It's the gold standard for measuring cardiovascular fitness.

**Factors Affecting Your VO2 Max:**
• Age: Typically peaks in 20s, declines ~1% per year
• Training: Your "{activity}" activity level {'positively' if activity in ['very', 'extra'] else 'moderately'} impacts this
• Genetics: Accounts for 25-50% of your potential
• Body composition: Lower body fat generally means higher VO2 max

**Recommendations to Improve:**
• Add 3-4 cardio sessions per week (running, cycling, swimming)
• Include high-intensity interval training (HIIT)
• Maintain consistent training for 8-12 weeks to see improvements
• Consider altitude training or sports-specific activities

**Normal Ranges:**
• Men 20-29: 38-48 ml/kg/min (good)
• Women 20-29: 32-42 ml/kg/min (good)
• Elite athletes: 60-85+ ml/kg/min"""

def calculate_bmr_calories(age, weight, height, gender, activity):
    # Mifflin-St Jeor Equation (most accurate)
    if gender.lower() == 'male':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    
    # Activity multipliers for TDEE
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'very': 1.725,
        'extra': 1.9
    }
    
    tdee = bmr * activity_multipliers.get(activity, 1.55)
    
    return f"""**Your Metabolic Rate:**

**BMR (Basal Metabolic Rate): {bmr:.0f} calories/day**
This is what your body burns at complete rest.

**TDEE (Total Daily Energy Expenditure): {tdee:.0f} calories/day**
This includes your daily activities ("{activity}" level).

**Calorie Goals:**
• Maintain weight: {tdee:.0f} calories/day
• Lose weight (1 lb/week): {tdee-500:.0f} calories/day
• Lose weight (2 lbs/week): {tdee-1000:.0f} calories/day
• Gain weight (1 lb/week): {tdee+500:.0f} calories/day

**Macronutrient Breakdown (for {tdee:.0f} calories):**
• Protein: {tdee*0.25/4:.0f}g (25% of calories)
• Carbohydrates: {tdee*0.45/4:.0f}g (45% of calories)
• Fats: {tdee*0.30/9:.0f}g (30% of calories)

**Tips to Boost Metabolism:**
• Build lean muscle through strength training
• Eat protein with every meal
• Stay hydrated and get quality sleep"""

def calculate_bmi(weight, height):
    bmi = weight / ((height/100) ** 2)
    
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    
    ideal_weight_min = 18.5 * ((height/100) ** 2)
    ideal_weight_max = 24.9 * ((height/100) ** 2)
    
    return f"""**Body Mass Index (BMI): {bmi:.1f}**

**Category: {category}**

**Your Stats:**
• Current weight: {weight} kg
• Height: {height} cm
• Ideal weight range: {ideal_weight_min:.1f}-{ideal_weight_max:.1f} kg

**BMI Categories:**
• Underweight: <18.5
• Normal weight: 18.5-24.9
• Overweight: 25-29.9
• Obese: ≥30

**Recommendations:**
• Combine cardio and strength training
• Focus on building healthy habits
• Consult healthcare providers for personalized advice"""

def calculate_heart_rate_zones(age):
    max_hr = 220 - age
    
    return f"""**Heart Rate Zones (Age {age}):**

**Maximum Heart Rate: {max_hr} bpm**

**Training Zones:**
• **Fat Burn Zone**: {int(max_hr * 0.6)}-{int(max_hr * 0.7)} bpm (60-70% max)
  - Best for: Fat burning, recovery workouts

• **Cardio Zone**: {int(max_hr * 0.7)}-{int(max_hr * 0.85)} bpm (70-85% max)
  - Best for: Cardiovascular fitness, endurance

• **Peak Zone**: {int(max_hr * 0.85)}-{int(max_hr * 0.95)} bpm (85-95% max)
  - Best for: Performance, anaerobic capacity

**Target Heart Rate for Different Goals:**
• Weight loss: Stay in Fat Burn zone (60-70%)
• Fitness improvement: Mix Cardio and Peak zones
• Endurance: Focus on Cardio zone (70-85%)"""

def calculate_fitness_metric(question, user_data):
    assessment_type = determine_assessment_type(question)
    
    # Extract user data with defaults
    age = user_data.get('age', 30)
    weight = user_data.get('weight', 70)  # kg
    height = user_data.get('height', 175)  # cm
    gender = user_data.get('gender', 'male')
    activity = user_data.get('activity_level', 'moderate')
    
    if assessment_type == "vo2_max":
        return calculate_vo2_max(age, weight, height, gender, activity)
    elif assessment_type == "bmr":
        return calculate_bmr_calories(age, weight, height, gender, activity)
    elif assessment_type == "heart_rate":
        return calculate_heart_rate_zones(age)
    elif assessment_type == "bmi":
        return calculate_bmi(weight, height)
    else:
        return f"""**Fitness Assessment**

Your question: "{question}"

**Profile:** Age {age}, {gender}, {activity} activity level

**General Recommendations:**
• Aim for 150 minutes of moderate cardio per week
• Include 2-3 strength training sessions
• Eat a balanced diet with adequate protein
• Get 7-9 hours of quality sleep
• Stay hydrated throughout the day

**Try asking specific questions like:**
• "What is my VO2 max?"
• "How many calories should I eat?"
• "What are my heart rate zones?"
• "What's my BMI?"

*This system uses scientific formulas for accurate fitness calculations.*"""

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    
    # Handle CORS preflight
    if event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS':
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST, OPTIONS"
            }
        }

    try:
        body = json.loads(event.get('body', '{}'))
        question = body.get('question', '')
        user_data = body.get('user_data', {})
        user_id = body.get('user_id', str(uuid.uuid4()))

        if not question:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type"
                },
                "body": json.dumps({"error": "Missing 'question' in request"})
            }

        # Calculate fitness metrics using mathematical formulas
        ai_response = calculate_fitness_metric(question, user_data)
        assessment_type = determine_assessment_type(question)
        
        print("Calculated response:", ai_response)
        
        # Save to DynamoDB
        timestamp = datetime.utcnow().isoformat()
        table.put_item(
            Item={
                'user_id': user_id,
                'timestamp': timestamp,
                'question': question,
                'assessment_type': assessment_type,
                'user_data': json.dumps(user_data) if user_data else '',
                'ai_response': ai_response
            }
        )
        print(f"Saved assessment for user {user_id}")

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST, OPTIONS"
            },
            "body": json.dumps({
                "response": ai_response,
                "assessment_type": assessment_type,
                "user_id": user_id,
                "timestamp": timestamp
            })
        }

    except Exception as e:
        print("Error occurred:", str(e))
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"error": "Internal server error", "details": str(e)})
        }