# Claim Status Error Analysis

Total Errors: 6/20

## Claim ID: user_002 (contradicted predicted instead of not_enough_information)
- **True Status**: not_enough_information
- **Pred Status**: contradicted
- **Evidence Met (True/Pred)**: False / True
- **Flags Triggered**: claim_mismatch;wrong_object
- **Issue (True/Pred)**: broken_part / unknown
- **Part (True/Pred)**: front_bumper / unknown
- **User Claim**: Customer: Parking lot mein meri car ko scrape lag gaya. | Support: Aap kis type ka damage report karna chahte hain? | Customer: Front side par mark aa gaya hai, bumper ke upar. | Support: Light damage hai ya body par scratch? | Customer: Light theek hai, front bumper par scratch hai. Photos upload kar diye hain.

## Claim ID: user_004 (contradicted predicted instead of supported)
- **True Status**: supported
- **Pred Status**: contradicted
- **Evidence Met (True/Pred)**: True / True
- **Flags Triggered**: claim_mismatch;blurry_image
- **Issue (True/Pred)**: crack / crack
- **Part (True/Pred)**: windshield / windshield
- **User Claim**: Customer: I am opening a claim for my windshield. | Support: What happened? | Customer: A small stone hit it while I was driving and now there is a crack spreading from that spot. | Support: Is the car otherwise okay? | Customer: Yes, this is only about the front glass. I added the pictures I have.

## Claim ID: user_005 (supported predicted instead of contradicted)
- **True Status**: contradicted
- **Pred Status**: supported
- **Evidence Met (True/Pred)**: True / True
- **Flags Triggered**: user_history_risk
- **Issue (True/Pred)**: scratch / dent
- **Part (True/Pred)**: rear_bumper / rear_bumper
- **User Claim**: Customer: I want to file this as bumper damage. | Support: Can you tell me what happened? | Customer: The car was tapped from behind and now the back looks damaged. | Support: Are you asking for review of the rear side? | Customer: Yes, the back bumper. It looks pretty bad to me, so I uploaded both photos.

## Claim ID: user_006 (contradicted predicted instead of not_enough_information)
- **True Status**: not_enough_information
- **Pred Status**: contradicted
- **Evidence Met (True/Pred)**: False / True
- **Flags Triggered**: wrong_object_part;damage_not_visible;wrong_angle
- **Issue (True/Pred)**: unknown / unknown
- **Part (True/Pred)**: headlight / unknown
- **User Claim**: Customer: Hi, I am not fully sure how to explain this because I noticed it only after reaching home. | Support: No problem, please tell me what happened. | Customer: There was a small bump earlier, nothing major, and I first thought everything was fine. Later I looked at the car again because my family member said the front area looked different. | Support: Are you reporting a general vehicle issue or a specific damaged part? | Customer: I was confused at first because I checked the side and the front and walked around the car a few times. I do not want to claim the wrong thing. | Support: That is okay. What part do you want reviewed? | Customer: After checking again, I think the issue is with the headlight. It looks like the headlight may be cracked, so please review that part.

## Claim ID: user_020 (supported predicted instead of contradicted)
- **True Status**: contradicted
- **Pred Status**: supported
- **Evidence Met (True/Pred)**: True / True
- **Flags Triggered**: user_history_risk
- **Issue (True/Pred)**: none / scratch
- **Part (True/Pred)**: trackpad / trackpad
- **User Claim**: Customer: The laptop trackpad has stopped working properly. | Support: Did anything happen before it stopped working? | Customer: The front area hit the desk edge when I moved it. | Support: Are you reporting internal function or physical damage? | Customer: Physical damage around the trackpad area. I attached the photo for review.

## Claim ID: user_032 (contradicted predicted instead of not_enough_information)
- **True Status**: not_enough_information
- **Pred Status**: contradicted
- **Evidence Met (True/Pred)**: False / True
- **Flags Triggered**: manual_review_required;damage_not_visible
- **Issue (True/Pred)**: unknown / unknown
- **Part (True/Pred)**: contents / unknown
- **User Claim**: Customer: The item I ordered was not inside the box. | Support: Did the package look opened when you received it? | Customer: I checked it after delivery and could not find the product inside. | Support: What are you asking us to verify? | Customer: Please verify that the contents are missing from the package.
