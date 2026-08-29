import re

medical_records = [
    {
        'patient_id': 'P1001',
        'age': 34,
        'gender': 'Female',
        'diagnosis': 'Hypertension',
        'medications': ['Lisinopril'],
        'last_visit_id': 'V2301',
    },
    {
        'patient_id': 'P1002',
        'age': 47,
        'gender': 'Male',
        'diagnosis': 'Type 2 Diabetes',
        'medications': ['Metformin', 'Insulin'],
        'last_visit_id': 'V2302',
    },
    {
        'patient_id': 'P1003',
        'age': 29,
        'gender': 'Female',
        'diagnosis': 'Asthma',
        'medications': ['Albuterol'],
        'last_visit_id': 'V2303',
    },
    {
        'patient_id': 'P1004',
        'age': 56,
        'gender': 'Male',
        'diagnosis': 'Chronic Back Pain',
        'medications': ['Ibuprofen', 'Physical Therapy'],
        'last_visit_id': 'V2304',
    }
]


def find_invalid_records(
        patient_id, age, gender, diagnosis, medications, last_visit_id
):
    constraints = {
        'patient_id': isinstance(patient_id, str)
                      and re.fullmatch(r'P\d{4}', patient_id),
        'age': isinstance(age, int) and age >= 18,
        'gender': isinstance(gender, str) and gender in ('Male', 'Female'),
        'diagnosis': isinstance(diagnosis, str) or diagnosis is None,
        'medications': isinstance(medications, list)
                       and all([isinstance(i, str) for i in medications]),
        'last_visit_id': isinstance(last_visit_id, str)
                         and re.fullmatch(r'V\d{4}', last_visit_id)
    }
    return [key for key, value in constraints.items() if not value]


def validate(data):
    is_sequence = isinstance(data, (list, tuple))

    if not is_sequence:
        print('Invalid format: expected a list or tuple.')
        return False

    is_invalid = False
    key_set = {
        'patient_id',
        'age',
        'gender',
        'diagnosis',
        'medications',
        'last_visit_id'
    }

    seen_id = set ()
    for record in data:
       patient_id = record['patient_id']
       if patient_id in seen_id:
           print(f'Duplicate patient id: {patient_id}')
           is_invalid = True
       else:
           seen_id.add(patient_id)

    for index, dictionary in enumerate(data):
        if not isinstance(dictionary, dict):
            print(f'Invalid format: expected a dictionary at position {index}.')
            is_invalid = True
            continue

        if set(dictionary.keys()) != key_set:
            print(
                f'Invalid format: {dictionary} at position {index} has missing and/or invalid keys.'
            )
            is_invalid = True
            continue

        invalid_records = find_invalid_records(**dictionary)
        for key in invalid_records:
            val = dictionary[key]
            print(f"Unexpected format '{key}: {val}' at position {index}.")
            is_invalid = True

    if is_invalid:
        return False
    print('Valid format.')
    return True


validate(medical_records)