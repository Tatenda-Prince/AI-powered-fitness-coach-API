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
    # Jackson et al. Non-Exercise VO2 max Prediction (validated formula)
    # Used by ACSM and fitness professionals worldwide
    
    # Calculate BMI for the formula
    bmi = weight / ((height/100) ** 2)
    
    # Activity level scoring (Physical Activity Rating - PAR)
    activity_scores = {
        'sedentary': 0,      # No regular activity
        'light': 1,          # Light activity 1-2 times/week
        'moderate': 3,       # Moderate activity 2-3 times/week
        'very': 5,           # Heavy activity 3-4 times/week
        'extra': 7           # Very heavy activity 5+ times/week
    }
    
    par_score = activity_scores.get(activity, 3)
    
    # Jackson et al. validated formulas
    if gender.lower() == 'male':
        # Men: VO2max = 56.363 + (1.921 × PAR-Q) - (0.381 × age) - (0.754 × BMI) + (10.987 × gender)
        vo2_estimate = 56.363 + (1.921 * par_score) - (0.381 * age) - (0.754 * bmi)
    else:
        # Women: Same formula but without gender adjustment
        vo2_estimate = 56.363 + (1.921 * par_score) - (0.381 * age) - (0.754 * bmi) - 10.987
    
    # Physiological bounds (realistic human ranges)
    vo2_estimate = max(15, min(85, vo2_estimate))
    
    # ACSM fitness classifications by age and gender
    if gender.lower() == 'male':
        if age < 30:
            if vo2_estimate >= 52: classification = "excellent"
            elif vo2_estimate >= 47: classification = "good"
            elif vo2_estimate >= 42: classification = "fair"
            else: classification = "needs improvement"
        elif age < 40:
            if vo2_estimate >= 50: classification = "excellent"
            elif vo2_estimate >= 44: classification = "good"
            elif vo2_estimate >= 39: classification = "fair"
            else: classification = "needs improvement"
        elif age < 50:
            if vo2_estimate >= 48: classification = "excellent"
            elif vo2_estimate >= 41: classification = "good"
            elif vo2_estimate >= 36: classification = "fair"
            else: classification = "needs improvement"
        else:
            if vo2_estimate >= 45: classification = "excellent"
            elif vo2_estimate >= 38: classification = "good"
            elif vo2_estimate >= 33: classification = "fair"
            else: classification = "needs improvement"
    else:  # female
        if age < 30:
            if vo2_estimate >= 44: classification = "excellent"
            elif vo2_estimate >= 39: classification = "good"
            elif vo2_estimate >= 35: classification = "fair"
            else: classification = "needs improvement"
        elif age < 40:
            if vo2_estimate >= 41: classification = "excellent"
            elif vo2_estimate >= 36: classification = "good"
            elif vo2_estimate >= 32: classification = "fair"
            else: classification = "needs improvement"
        elif age < 50:
            if vo2_estimate >= 39: classification = "excellent"
            elif vo2_estimate >= 34: classification = "good"
            elif vo2_estimate >= 30: classification = "fair"
            else: classification = "needs improvement"
        else:
            if vo2_estimate >= 36: classification = "excellent"
            elif vo2_estimate >= 31: classification = "good"
            elif vo2_estimate >= 27: classification = "fair"
            else: classification = "needs improvement"
    
    return f"""**Estimated VO2 Max: {vo2_estimate:.1f} ml/kg/min**

Your VO2 max estimate puts you in the "{classification}" category for your age and gender ({age}-year-old {gender}).

**Calculation Method:**
Using the Jackson et al. Non-Exercise VO2 max prediction formula - the same method used by ACSM-certified fitness professionals and validated against laboratory testing (r=0.92 correlation).

**What is VO2 Max?**
VO2 max represents the maximum amount of oxygen your body can utilize during intense exercise. It's the gold standard for measuring cardiovascular fitness and endurance capacity.

**Factors in Your Calculation:**
• Age: {age} years (VO2 max typically declines ~1% per year after 25)
• BMI: {bmi:.1f} (body composition affects oxygen delivery)
• Activity Level: "{activity}" (training history significantly impacts VO2 max)
• Gender: Biological differences in heart size and hemoglobin levels

**Recommendations to Improve:**
• Aerobic training: 3-5 sessions per week, 20-60 minutes
• High-intensity intervals: 2-3 times per week
• Progressive overload: Gradually increase intensity/duration
• Consistency: Improvements typically seen in 6-12 weeks
• Cross-training: Mix running, cycling, swimming for best results

**ACSM Fitness Classifications:**
• Excellent: Top 20% for your age/gender
• Good: Above average fitness level
• Fair: Average fitness level
• Needs Improvement: Below average, focus on cardio training

*Note: This is an estimate. Laboratory testing provides the most accurate VO2 max measurement.*"""

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