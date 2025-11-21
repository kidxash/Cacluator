import json

def lambda_handler(event, context):

    
    # CORS headers - allows web browsers to call this function
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    # Handle OPTIONS request (browser preflight check)
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'OK'})
        }
    
    try:
        # Get data from request
        if 'body' in event:
            data = json.loads(event['body'])
        else:
            data = event
        
        # Extract student ID and grades
        student_id = data.get('student_id', '')
        grades = data.get('grades', [])
        
        # Validate student ID
        if not student_id or not student_id.strip():
            raise ValueError('Student ID is required')
        
        # Validate grades
        if not grades or len(grades) == 0:
            raise ValueError('At least one grade is required')
        
        # Check each grade is valid
        for i, grade in enumerate(grades):
            if not isinstance(grade, (int, float)):
                raise ValueError(f'Grade {i+1} must be a number')
            if grade < 0 or grade > 100:
                raise ValueError(f'Grade {i+1} must be between 0 and 100')
        
        # Calculate average
        total = sum(grades)
        average = total / len(grades)
        average = round(average, 2)  # Round to 2 decimal places
        
        # Return success response
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'success': True,
                'student_id': student_id.strip(),
                'grades': grades,
                'average': average,
                'grade_count': len(grades),
                'message': f'Successfully calculated average for {student_id.strip()}'
            })
        }
        
    except ValueError as e:
        # Return error for validation failures
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({
                'success': False,
                'message': str(e)
            })
        }
    except Exception as e:
        # Return error for unexpected failures
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'success': False,
                'message': 'Internal server error: ' + str(e)
            })
        }

# Test locally (optional)
if __name__ == '__main__':
    # Test with sample data
    test_event = {
        'student_id': 'S123456',
        'grades': [85, 90, 78]
    }
    
    result = lambda_handler(test_event, None)
    print('Test Result:')
    print(json.dumps(json.loads(result['body']), indent=2))
