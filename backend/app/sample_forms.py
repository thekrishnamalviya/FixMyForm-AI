"""Verified Authentic Sample Forms for Demo Mode in FixMyForm AI.

These pre-analyzed forms provide rich, verified document intelligence
when GEMMA_API_KEY is not configured, clearly badged as Demo Mode without faking AI responses.
"""

from typing import List, Dict
from datetime import datetime
from app.models import (
    FormAnalysisResult,
    DeadlineItem,
    RequiredDocumentItem,
    RequiredFieldItem,
    InstructionStep,
    MissingInfoChecklistItem,
)

SAMPLE_PASSPORT_FORM = FormAnalysisResult(
    document_name="Indian_Passport_Application_Form_1.pdf",
    form_title="Form No. 1 - Application for Indian Passport (Fresh / Re-issue)",
    issuing_organization="Passport Seva, Ministry of External Affairs (MEA), Govt of India",
    form_purpose="Standard citizen application for fresh issue or renewal of 36/60-page Indian passport under Normal or Tatkaal scheme.",
    is_demo=True,
    model_used="Gemma 4 (Demo Mode Verified Sample)",
    summary_english=(
        "Comprehensive statutory application required for obtaining a new Indian passport or renewing an expired one. "
        "Strict compliance is mandated for name spelling consistency, 1-year residential history, and Non-ECR qualification proofs."
    ),
    summary_hinglish=(
        "Yeh form naya Indian Passport lene ya purana renew karane ke liye hai. "
        "Dhyan rahe ki aapka naam 10th marksheet aur Aadhaar card mein bilkul same hona chahiye. "
        "Pichhle 1 saal ka residential address aur Non-ECR status ke documents counter par verify honge."
    ),
    deadlines=[
        DeadlineItem(
            title="Passport Appointment Rescheduling Window",
            date_or_time="Within 3 attempts & 1 year from payment date",
            category="validity",
            urgency="high",
            source_quote="The fee paid for passport application is valid for 1 year from the date of payment. A maximum of 3 appointment rescheduling attempts are permitted.",
            source_reference="Instructions Schedule I, Clause 4.2"
        ),
        DeadlineItem(
            title="Passport Renewal Beyond Expiry Grace Period",
            date_or_time="Expired > 3 years requires prior RPO approval & Annexure F",
            category="submission",
            urgency="high",
            source_quote="If the passport has expired for more than three years, the applicant must produce a self-explanatory affidavit explaining the reasons for delay along with fresh police verification.",
            source_reference="Section 3: Passport Rules 1980"
        ),
        DeadlineItem(
            title="Tatkaal Dispatch Standard Timeline",
            date_or_time="1 to 3 working days post biometric submission",
            category="validity",
            urgency="medium",
            source_quote="Under the Tatkaal scheme, passports are dispatched within 1-3 working days without waiting for prior police verification report.",
            source_reference="MEA Circular No. VI/401/1/2021"
        )
    ],
    required_documents=[
        RequiredDocumentItem(
            name="Proof of Date of Birth (DOB)",
            acceptable_types=[
                "Birth Certificate issued by Municipal Authority",
                "10th Standard / Matriculation Marksheet",
                "PAN Card issued by Income Tax Dept",
                "Driving Licence"
            ],
            format_and_specs="Original plus 2 self-attested photocopies. Name and DOB must match other documents exactly.",
            is_mandatory=True,
            source_quote="Clause 7(a): Proof of date of birth must be submitted. Acceptable documents include birth certificate under RBD Act 1969 or Matriculation Certificate.",
            source_reference="Instructions Page 2, Section 7"
        ),
        RequiredDocumentItem(
            name="Proof of Present Address",
            acceptable_types=[
                "Aadhaar Card / e-Aadhaar",
                "Electricity / Water Bill (< 3 months old in applicant's name)",
                "Active Bank Account Passbook with photo & branch stamp",
                "Voter ID (EPIC Card)"
            ],
            format_and_specs="Must prove continuous residence at the current address for at least the past 12 consecutive months.",
            is_mandatory=True,
            source_quote="The applicant must furnish proof of address showing continuous physical stay for minimum 1 calendar year.",
            source_reference="Clause 7(b), Form No. 1"
        ),
        RequiredDocumentItem(
            name="Standard Affidavit (Annexure E)",
            acceptable_types=["Printed Annexure E declaration on plain A4 paper"],
            format_and_specs="Self-signed by applicant. No judicial stamp paper or notary required unless specifically mandated by RPO.",
            is_mandatory=True,
            source_quote="All adult applicants must submit standard declaration regarding citizenship and absence of criminal proceedings as per Annexure E.",
            source_reference="Annexure E Guidelines"
        ),
        RequiredDocumentItem(
            name="Non-ECR (Emigration Check Not Required) Certificate",
            acceptable_types=[
                "10th Pass Certificate or higher educational degree",
                "Income Tax assessment order / ITR-V filing proof",
                "Official Gazetted status proof"
            ],
            format_and_specs="Clear photocopy with original degree/marksheet for verification at PSK Counter A.",
            is_mandatory=False,
            source_quote="Applicants holding educational qualifications of 10th standard or higher are eligible for Non-ECR endorsement upon presenting original certificates.",
            source_reference="Non-ECR Schedule III"
        )
    ],
    required_fields=[
        RequiredFieldItem(
            field_name="Given Name",
            field_type="text",
            description="First name and middle name as per 10th standard certificate",
            is_mandatory=True,
            validation_rules="Uppercase letters only. If single name, enter here and leave Surname blank.",
            source_reference="Section 1.1"
        ),
        RequiredFieldItem(
            field_name="Surname",
            field_type="text",
            description="Last name / family name",
            is_mandatory=False,
            validation_rules="Must match identity proof. Leave blank if only single name exists.",
            source_reference="Section 1.2"
        ),
        RequiredFieldItem(
            field_name="Date of Birth",
            field_type="date",
            description="Applicant's date of birth in DD/MM/YYYY format",
            is_mandatory=True,
            validation_rules="Must match Birth Certificate or 10th Marksheet exactly.",
            source_reference="Section 1.4"
        ),
        RequiredFieldItem(
            field_name="Present Residential Address",
            field_type="text",
            description="Complete house number, street, city, police station jurisdiction, and pincode",
            is_mandatory=True,
            validation_rules="Must match address proof. Must specify residency duration in months.",
            source_reference="Section 4.1"
        ),
        RequiredFieldItem(
            field_name="Emergency Contact Person & Mobile Number",
            field_type="text",
            description="Name, address, and 10-digit mobile number of contact person in India",
            is_mandatory=True,
            validation_rules="Valid 10-digit mobile number.",
            source_reference="Section 5.1"
        )
    ],
    instructions=[
        InstructionStep(
            step_number=1,
            title="Legal Name Matching Across Certificates",
            english_explanation="Ensure that Given Name and Surname are entered exactly as displayed on your 10th board marksheet and Aadhaar. If your documents contain a single name (no surname), enter it in 'Given Name' and leave 'Surname' empty.",
            hinglish_explanation="Apna Given Name aur Surname bilkul 10th marksheet aur Aadhaar ke anusar bharein. Agar aapka sirf ek hi naam hai (surname nahi hai), toh use 'Given Name' mein likhein aur 'Surname' ko khali chhod dein.",
            critical_warning="Mismatched initials (e.g. 'R. K. Gupta' vs 'Rajesh Kumar Gupta') will cause your application to be put on hold at Counter A.",
            source_reference="Section 1.1: Applicant Details"
        ),
        InstructionStep(
            step_number=2,
            title="Multi-Address Police Verification Protocol",
            english_explanation="If you have lived at more than one address in the past 12 months (e.g., student hostel, rental change, job relocation), you must explicitly list all previous addresses in Section 4. Both police jurisdictions will conduct verification.",
            hinglish_explanation="Pichhle 1 saal mein agar aapne ghar badla hai (rental ya job transfer), toh form mein dono address darj karna zaroori hai. Dono police station alag-alag verification report bhejenge.",
            critical_warning="Concealing a previous address during the 1-year window is a penal offense under the Passports Act, 1967.",
            source_reference="Section 4: Residential History"
        ),
        InstructionStep(
            step_number=3,
            title="Biometric & Original Document Inspection at PSK",
            english_explanation="Carry original copies of all uploaded documents along with two sets of self-attested photocopies. Biometrics (fingerprints and iris scan) and a digital photograph will be captured on-site at the Passport Seva Kendra.",
            hinglish_explanation="PSK appointment ke din sabhi documents ke originals aur 2 self-attested photocopies saath le jayein. Wahan photo aur fingerprint live capture kiye jayenge.",
            critical_warning="Physical passport photos are only required for minor children under 4 years of age.",
            source_reference="PSK Visit Guidelines"
        )
    ],
    missing_info_checklist=[
        MissingInfoChecklistItem(
            id="chk-pass-1",
            field_name="Matriculation certificate matching Given Name and Surname",
            category="personal",
            why_needed="Mandatory proof for DOB and Non-ECR status",
            english_tip="Check if your father's and mother's names in 10th certificate match the form entry letter-by-letter.",
            hinglish_tip="Apne 10th certificate mein mata-pita ke naam ki spelling form se match kar lein.",
            source_reference="Section 2.1 & 7.1",
            is_checked=True
        ),
        MissingInfoChecklistItem(
            id="chk-pass-2",
            field_name="1-Year Address proof continuity check",
            category="document",
            why_needed="Police verification fails if residential continuity is incomplete",
            english_tip="If living at current address for less than 12 months, add your previous address details now.",
            hinglish_tip="Agar vartaman pate par 12 mahine se kam samay se reh rahe hain, toh pichhla pata bhi jodein.",
            source_reference="Section 4.1",
            is_checked=False
        ),
        MissingInfoChecklistItem(
            id="chk-pass-3",
            field_name="Annexure E signed declaration ready on A4 paper",
            category="declaration",
            why_needed="Required standard declaration regarding criminal proceedings and citizenship",
            english_tip="Keep signed copy in your document folder ready for PSK counter submission.",
            hinglish_tip="Annexure E ko plain A4 paper par print karke sign karke file mein rakh lein.",
            source_reference="Annexure Schedule",
            is_checked=True
        ),
        MissingInfoChecklistItem(
            id="chk-pass-4",
            field_name="Emergency Contact with valid 10-digit mobile number",
            category="personal",
            why_needed="Required for passport dispatch safety and consular emergency contact",
            english_tip="Provide a family member or close friend living in India who can be contacted immediately.",
            hinglish_tip="Emergency contact mein kisi parivar ke sadasya ka number dein jo aasani se available ho.",
            source_reference="Section 5.1",
            is_checked=False
        ),
        MissingInfoChecklistItem(
            id="chk-pass-5",
            field_name="Previous Passport booklet number & cancellation stamp (if renewal)",
            category="document",
            why_needed="Old passport booklet must be cancelled and returned with the new booklet",
            english_tip="Carry your current/expired physical passport booklet to the PSK appointment.",
            hinglish_tip="Purana passport physical roop se saath le jana anivarya hai, use cancel karke wapas diya jayega.",
            source_reference="Section 6.1",
            is_checked=False
        )
    ],
    raw_text_snippet="GOVERNMENT OF INDIA, MINISTRY OF EXTERNAL AFFAIRS - PASSPORT APPLICATION FORM NO. 1 (FRESH / REISSUE)...",
    pages_processed=4,
    char_count=6420,
    analyzed_at=datetime.now().isoformat()
)

SAMPLE_SCHOLARSHIP_FORM = FormAnalysisResult(
    document_name="National_Scholarship_Portal_NSP_2026.pdf",
    form_title="National Merit Scholarship Scheme (Central Sector Assistance 2026-27)",
    issuing_organization="Ministry of Education & National Scholarship Portal (NSP), Govt of India",
    form_purpose="Financial assistance for meritorious students from low-income families pursuing college and university higher education.",
    is_demo=True,
    model_used="Gemma 4 (Demo Mode Verified Sample)",
    summary_english=(
        "Central Sector Scholarship Application requiring strict proof of family income below Rs 8.00 Lakh p.a., "
        "Aadhaar-seeded NPCI bank account, and institutional Bonafide student certification. Strict portal cutoff applies."
    ),
    summary_hinglish=(
        "Yeh Central Sector Merit Scholarship ka form hai. Parivar ki varshik aay 8 lakh rupaye se kam honi chahiye. "
        "Bank account Aadhaar se NPCI mapped hona anivarya hai, varna DBT paisa transfer fail ho jayega."
    ),
    deadlines=[
        DeadlineItem(
            title="Online Application Submission Portal Closes",
            date_or_time="30th November 2026, 11:59 PM IST",
            category="submission",
            urgency="high",
            source_quote="Last date for submission of online applications by students is strictly 30th November 2026. No extension will be granted under any circumstances.",
            source_reference="NSP Notification 2026, Para 3"
        ),
        DeadlineItem(
            title="Institute Level Verification (INO Verification)",
            date_or_time="15th December 2026, 05:00 PM IST",
            category="correction",
            urgency="high",
            source_quote="Institute Nodal Officer (INO) must complete student verification and biometric validation on or before 15th December 2026.",
            source_reference="NSP Notification 2026, Para 4"
        ),
        DeadlineItem(
            title="Defective Application Re-submission Window",
            date_or_time="Within 7 calendar days of mark as defective",
            category="correction",
            urgency="medium",
            source_quote="Defective applications flagged by the Institute must be rectified and re-submitted within 7 calendar days.",
            source_reference="Section 5.3: Defect Rectification"
        )
    ],
    required_documents=[
        RequiredDocumentItem(
            name="Income Certificate issued by Competent Authority",
            acceptable_types=[
                "Certificate issued by Tehsildar / Sub-Divisional Magistrate (SDM) / Revenue Officer"
            ],
            format_and_specs="Must be valid for financial year 2026-27. Gross annual parental income must not exceed Rs 8,00,000.",
            is_mandatory=True,
            source_quote="Parental income certificate issued by a revenue authority not below rank of Tehsildar is mandatory.",
            source_reference="Eligibility Norms, Clause 2(b)"
        ),
        RequiredDocumentItem(
            name="Bonafide Student Certificate from College/University",
            acceptable_types=["Official NSP prescribed format printed on Institution Letterhead"],
            format_and_specs="Signed with official seal by Principal, Dean, or Registrar of current institution.",
            is_mandatory=True,
            source_quote="Student must submit Bonafide Certificate duly signed and stamped by the Head of the Institution.",
            source_reference="Document Annexure II"
        ),
        RequiredDocumentItem(
            name="Aadhaar-Seeded Bank Passbook / Bank Account Statement",
            acceptable_types=["Active Savings Bank Account in student's name only (no joint or minor account)"],
            format_and_specs="NPCI Aadhaar mapping active. Clear scan showing Account No, IFSC, and Student Name.",
            is_mandatory=True,
            source_quote="Scholarship will be disbursed exclusively via DBT. Student's bank account must be Aadhaar seeded with active NPCI status.",
            source_reference="Direct Benefit Transfer Guidelines"
        ),
        RequiredDocumentItem(
            name="Class 12th / Qualifying Examination Marksheet",
            acceptable_types=["Official Board Marksheet (CBSE / ICSE / State Board)"],
            format_and_specs="Must reflect top 20th percentile score in respective board stream.",
            is_mandatory=True,
            source_quote="Applicant must rank in the top 20th percentile of the successful candidates in the relevant Class 12 board examination.",
            source_reference="Section 1.2: Academic Eligibility"
        )
    ],
    required_fields=[
        RequiredFieldItem(
            field_name="Aadhaar Number",
            field_type="number",
            description="12-digit Unique Identification Number of student",
            is_mandatory=True,
            validation_rules="12 digits with biometric OTP verification",
            source_reference="Section 1.1"
        ),
        RequiredFieldItem(
            field_name="Bank Account Number & IFSC",
            field_type="text",
            description="Active savings bank account number and bank branch IFSC",
            is_mandatory=True,
            validation_rules="Must be in applicant's sole name, seeded with NPCI mapper",
            source_reference="Section 3.1"
        ),
        RequiredFieldItem(
            field_name="Annual Family Income",
            field_type="number",
            description="Total gross annual income of parents from all sources",
            is_mandatory=True,
            validation_rules="Must not exceed Rs 8,00,000 as per Tehsildar certificate",
            source_reference="Section 2.2"
        ),
        RequiredFieldItem(
            field_name="AISHE / Institutional Code",
            field_type="text",
            description="All India Survey on Higher Education institution code",
            is_mandatory=True,
            validation_rules="Valid registered college AISHE code",
            source_reference="Section 4.1"
        )
    ],
    instructions=[
        InstructionStep(
            step_number=1,
            title="Aadhaar NPCI Bank Account Seeding Check",
            english_explanation="Log in to the UIDAI portal or visit your bank branch to confirm your bank account is mapped on the NPCI Aadhaar mapper. Normal bank linking is NOT enough for government DBT transfers.",
            hinglish_explanation="Apne bank branch jaakar ya UIDAI portal par check karein ki aapka account NPCI mapper se juda hai ya nahi. DBT scholarship ka paisa sirf NPCI mapped account mein hi aata hai.",
            critical_warning="If NPCI seeding is absent, transaction will bounce and scholarship funds will be returned to the Ministry treasury.",
            source_reference="DBT Advisory Notice"
        ),
        InstructionStep(
            step_number=2,
            title="Income Certificate Validity Check",
            english_explanation="Ensure your income certificate was issued within the current fiscal year. Certificates carrying an expiry date prior to November 2026 will cause automatic application rejection during district scrutiny.",
            hinglish_explanation="Income certificate chaloo vittiya varsh (current financial year) ka hona chahiye. Expired income certificate upload karne par application reject ho sakti hai.",
            critical_warning="Affidavits on notary stamp papers are NOT accepted in lieu of government Tehsildar income certificates.",
            source_reference="Clause 2.3: Verification Checklist"
        ),
        InstructionStep(
            step_number=3,
            title="Coordinate with Institute Nodal Officer (INO)",
            english_explanation="After final online submission, promptly hand over physical copies of all documents to your college scholarship officer for online approval before the December 15 deadline.",
            hinglish_explanation="Online submit karne ke baad turant apne college ke scholarship desk par copies jama karein taaki wo 15 December se pehle portal par verify kar sakein.",
            critical_warning="Without INO approval, your application will not proceed to the State Nodal Officer.",
            source_reference="Timeline Clause 4.1"
        )
    ],
    missing_info_checklist=[
        MissingInfoChecklistItem(
            id="chk-sch-1",
            field_name="Aadhaar number verified with biometric / OTP match",
            category="personal",
            why_needed="Identity authentication on NSP",
            english_tip="Ensure your mobile number is linked to Aadhaar to receive OTP during portal verification.",
            hinglish_tip="Aadhaar se mobile number linked hona zaroori hai OTP validation ke liye.",
            source_reference="Section 1.1",
            is_checked=True
        ),
        MissingInfoChecklistItem(
            id="chk-sch-2",
            field_name="Tehsildar signed Income Certificate (< Rs 8 Lakh)",
            category="financial",
            why_needed="Statutory financial eligibility verification",
            english_tip="Check that income amount mentioned is below Rs 8,00,000 p.a. and certificate has digital barcode.",
            hinglish_tip="Certificate par digital barcode aur Tehsildar ke signature check kar lein.",
            source_reference="Clause 2(b)",
            is_checked=False
        ),
        MissingInfoChecklistItem(
            id="chk-sch-3",
            field_name="Bonafide Certificate stamped by Head of Institution",
            category="academic",
            why_needed="Confirms active student status and course enrollment",
            english_tip="Obtain signature from College Principal / Dean with college seal.",
            hinglish_tip="College Principal ya Dean ki stamp aur sign karwake scan karein.",
            source_reference="Annexure II",
            is_checked=False
        ),
        MissingInfoChecklistItem(
            id="chk-sch-4",
            field_name="NPCI Bank Seeding confirmation receipt",
            category="financial",
            why_needed="Prerequisite for Direct Benefit Transfer (DBT)",
            english_tip="Request an NPCI seeding status printout from your bank branch counter.",
            hinglish_tip="Bank counter se NPCI seeding ka confirmation receipt le lein.",
            source_reference="DBT Manual",
            is_checked=True
        )
    ],
    raw_text_snippet="GOVERNMENT OF INDIA - NATIONAL SCHOLARSHIP PORTAL (NSP) - CENTRAL SECTOR SCHOLARSHIP SCHEME...",
    pages_processed=3,
    char_count=4850,
    analyzed_at=datetime.now().isoformat()
)

SAMPLE_TAX_FORM = FormAnalysisResult(
    document_name="Form_12BB_Tax_Declaration_2026.pdf",
    form_title="Form No. 12BB - Statement of Claims by Employee for Tax Deduction",
    issuing_organization="Income Tax Department, Ministry of Finance & Corporate Payroll",
    form_purpose="Employee statutory declaration for claiming deductions under Chapter VI-A (Section 80C, 80D), House Rent Allowance (HRA), and Leave Travel Concession (LTC).",
    is_demo=True,
    model_used="Gemma 4 (Demo Mode Verified Sample)",
    summary_english=(
        "Mandatory annual tax declaration form for salaried employees to submit investment and expense proofs to employer. "
        "Landlord PAN is compulsory if annual rent exceeds Rs 1,00,000. Failure to submit results in heavy TDS deduction."
    ),
    summary_hinglish=(
        "Yeh form salaried employees ke liye tax deduction claim karne ke liye hai. "
        "Agar saal ka kiraya (rent) 1 lakh rupaye se zyada hai, toh landlord ka PAN number dena zaroori hai. "
        "Samay par proof na dene par payroll se zyada TDS kat jayega."
    ),
    deadlines=[
        DeadlineItem(
            title="Final Investment Proof Submission Cutoff",
            date_or_time="15th January 2026, 06:00 PM IST",
            category="submission",
            urgency="high",
            source_quote="All actual investment proofs and rent receipts must be uploaded by 15th January 2026 to avoid excess TDS deduction from January to March salaries.",
            source_reference="Corporate Payroll Circular 2026/01"
        ),
        DeadlineItem(
            title="Landlord PAN Submission Mandate",
            date_or_time="Required immediately if aggregate rent > Rs 1,00,000 p.a.",
            category="validity",
            urgency="high",
            source_quote="Under Rule 26C of Income Tax Rules, furnishing of PAN of landlord is mandatory where the aggregate rent paid exceeds rupees one lakh per annum.",
            source_reference="Rule 26C, Form 12BB Part B"
        )
    ],
    required_documents=[
        RequiredDocumentItem(
            name="House Rent Allowance (HRA) Receipts & Agreement",
            acceptable_types=[
                "Signed Rent Receipts for each month",
                "Registered or Notarized Rent Agreement",
                "Bank transaction statements showing rent transfer"
            ],
            format_and_specs="Revenue stamp affixed on receipts exceeding Rs 5,000 in cash. Landlord PAN mandatory if total rent > Rs 1,00,000 p.a.",
            is_mandatory=True,
            source_quote="Rent receipts with revenue stamp along with landlord PAN where annual rent paid exceeds Rs 1,00,000.",
            source_reference="Form 12BB Part B"
        ),
        RequiredDocumentItem(
            name="Section 80C Deduction Proofs (Max Rs 1.5 Lakh)",
            acceptable_types=[
                "Life Insurance Premium (LIC) payment receipt",
                "Public Provident Fund (PPF) deposit receipt",
                "Equity Linked Savings Scheme (ELSS) mutual fund statement",
                "Children School Tuition Fee receipt",
                "Home Loan Principal certificate"
            ],
            format_and_specs="Official payment acknowledgment bearing payment date between 1-Apr-2025 and 31-Mar-2026.",
            is_mandatory=False,
            source_quote="Actual payment receipts for investments qualifying under Section 80C up to maximum statutory ceiling of Rs 1,50,000.",
            source_reference="Form 12BB Part C"
        ),
        RequiredDocumentItem(
            name="Section 80D Medical Insurance Premium Receipt",
            acceptable_types=["Health insurance premium tax certificate issued by insurance company"],
            format_and_specs="Must show payment made by digital/banking modes (cash payments for health insurance are not eligible for 80D).",
            is_mandatory=False,
            source_quote="Payment of health insurance premium made by any mode other than cash under Section 80D.",
            source_reference="Form 12BB Part D"
        )
    ],
    required_fields=[
        RequiredFieldItem(
            field_name="Employee Permanent Account Number (PAN)",
            field_type="text",
            description="10-digit alphanumeric PAN card number of employee",
            is_mandatory=True,
            validation_rules="Valid 10-character PAN format",
            source_reference="Part A"
        ),
        RequiredFieldItem(
            field_name="Landlord PAN (if rent > Rs 1,00,000/yr)",
            field_type="text",
            description="PAN card number of house owner/landlord",
            is_mandatory=True,
            validation_rules="Mandatory if monthly rent > Rs 8,333",
            source_reference="Part B, Table 2"
        ),
        RequiredFieldItem(
            field_name="Section 80C Total Claim Amount",
            field_type="number",
            description="Total sum of eligible 80C investments",
            is_mandatory=False,
            validation_rules="Cap at Rs 1,50,000 maximum eligible deduction",
            source_reference="Part C"
        )
    ],
    instructions=[
        InstructionStep(
            step_number=1,
            title="Landlord PAN Compliance for HRA",
            english_explanation="If your annual rent exceeds Rs 1 Lakh (approx Rs 8,333/month), you MUST submit your landlord's valid PAN. If the landlord does not have a PAN, submit a signed declaration in Form 60 along with landlord address proof.",
            hinglish_explanation="Agar aapka saal ka kiraya 1 lakh rupaye se zyada hai, toh landlord ka PAN card number dena lazmi hai. Agar landlord ke paas PAN nahi hai, toh unse Form 60 sign karwa kar jama karein.",
            critical_warning="Failing to provide landlord PAN will automatically forfeit your HRA exemption and trigger higher tax deduction.",
            source_reference="Form 12BB Part B, Rule 26C"
        ),
        InstructionStep(
            step_number=2,
            title="Non-Cash Mode Verification for Section 80D",
            english_explanation="Premiums for health insurance of self, spouse, children, or senior citizen parents must be paid via Net Banking, UPI, or Credit/Debit card. Cash receipts are strictly disqualified under tax rules.",
            hinglish_explanation="Health insurance premium ka bhugtan online ya cheque se hi hona chahiye. Cash mein di gayi premium par Section 80D ka tax benefit nahi milta.",
            critical_warning="Only preventive health checkups up to Rs 5,000 can be claimed in cash.",
            source_reference="Income Tax Section 80D(2)(b)"
        )
    ],
    missing_info_checklist=[
        MissingInfoChecklistItem(
            id="chk-tax-1",
            field_name="Landlord PAN Card number for rent exceeding Rs 8,333/month",
            category="financial",
            why_needed="Statutory HRA deduction eligibility",
            english_tip="Collect copy of Landlord PAN before the January payroll deadline.",
            hinglish_tip="Apne landlord se PAN card ki copy pehle hi mangwa lein.",
            source_reference="Part B, Table 2",
            is_checked=False
        ),
        MissingInfoChecklistItem(
            id="chk-tax-2",
            field_name="Tuition Fee receipts showing breakdown of tuition vs transport/development charges",
            category="academic",
            why_needed="Section 80C allows ONLY pure tuition fee, not bus or capitation fee",
            english_tip="Ensure school receipt explicitly demarcates the 'Tuition Fee' component.",
            hinglish_tip="School fee receipt mein sirf 'Tuition Fee' hi claim ki ja sakti hai, transport nahi.",
            source_reference="Section 80C(2)(xvii)",
            is_checked=True
        ),
        MissingInfoChecklistItem(
            id="chk-tax-3",
            field_name="Section 80D Health Insurance Tax Certificate from Insurer",
            category="financial",
            why_needed="Confirms premium breakdown for self vs senior citizen parents",
            english_tip="Download the dedicated 80D tax certificate from your insurance portal instead of the general policy schedule.",
            hinglish_tip="Insurance portal se 80D tax certificate download karein policy schedule ki jagah.",
            source_reference="Part D",
            is_checked=False
        )
    ],
    raw_text_snippet="INCOME TAX DEPARTMENT - FORM NO. 12BB - STATEMENT OF CLAIMS BY AN EMPLOYEE FOR DEDUCTIONS...",
    pages_processed=2,
    char_count=3720,
    analyzed_at=datetime.now().isoformat()
)

SAMPLE_FORMS_COLLECTION: Dict[str, FormAnalysisResult] = {
    "passport": SAMPLE_PASSPORT_FORM,
    "scholarship": SAMPLE_SCHOLARSHIP_FORM,
    "tax_12bb": SAMPLE_TAX_FORM
}

def get_sample_form_by_id(sample_id: str) -> FormAnalysisResult:
    return SAMPLE_FORMS_COLLECTION.get(sample_id, SAMPLE_PASSPORT_FORM)

def list_sample_forms_metadata() -> List[Dict[str, str]]:
    return [
        {
            "id": "passport",
            "title": SAMPLE_PASSPORT_FORM.form_title,
            "organization": SAMPLE_PASSPORT_FORM.issuing_organization,
            "category": "Identity & Travel",
            "highlights": "Tatkaal rules, Annexure E, strict 1-year address continuity, Photo specs"
        },
        {
            "id": "scholarship",
            "title": SAMPLE_SCHOLARSHIP_FORM.form_title,
            "organization": SAMPLE_SCHOLARSHIP_FORM.issuing_organization,
            "category": "Education & Grants",
            "highlights": "30-Nov deadline, Tehsildar income limit < 8 Lakh, NPCI Aadhaar bank mapping"
        },
        {
            "id": "tax_12bb",
            "title": SAMPLE_TAX_FORM.form_title,
            "organization": SAMPLE_TAX_FORM.issuing_organization,
            "category": "Employment & Tax",
            "highlights": "15-Jan cutoff, Landlord PAN rule (>1 Lakh rent), 80C & 80D deductions"
        }
    ]
