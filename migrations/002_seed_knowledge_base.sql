-- ClinicDesk AI — Knowledge Base Seed Data
-- 67 articles across 7 categories

-- =============================================================================
-- SCHEDULING (10 articles)
-- =============================================================================

INSERT INTO knowledge_articles (title, slug, category, content) VALUES

('How to Book a New Appointment',
'how-to-book-a-new-appointment',
'scheduling',
'## How to Book a New Appointment

Use ClinicDesk''s calendar to quickly schedule patients with the right provider at the right time.

## Steps to Book an Appointment

1. Navigate to the **Schedule** module from the left sidebar.
2. Click the **+ New Appointment** button in the top-right corner of the calendar view, or click directly on an available time slot.
3. In the **New Appointment** panel that slides in from the right, begin typing the patient''s name in the **Patient** field. Select the correct patient from the autocomplete dropdown.
4. If the patient is new and does not appear, click **Create New Patient** to open the patient registration form without leaving the scheduler.
5. Select the **Provider** from the dropdown. Only providers marked as available for the selected time slot will appear.
6. Choose the **Appointment Type** (e.g., New Patient Exam, Recall Cleaning, Emergency Visit). The duration field will auto-populate based on your configured defaults.
7. Adjust the **Date** and **Start Time** if needed using the date/time pickers.
8. Add any **Notes** relevant to the visit in the Internal Notes field.
9. Select a **Operatory** or room if your clinic uses operatory management.
10. Click **Save Appointment** to confirm the booking.

## Confirmation and Notifications

- The appointment will immediately appear on the calendar grid.
- If automated reminders are enabled, the patient will receive a confirmation via their preferred contact method (email or SMS).
- A confirmation number is displayed in the appointment detail panel for reference.

## Tips

- Use the **Quick Book** shortcut (Ctrl+N / Cmd+N) to open the New Appointment panel from anywhere in ClinicDesk.
- Color coding on the calendar reflects appointment type. Configure colors under **Settings → Scheduling → Appointment Types**.
- If the selected time slot is unavailable, ClinicDesk will highlight the nearest open slot in green.'),

('How to Reschedule an Existing Appointment',
'how-to-reschedule-an-existing-appointment',
'scheduling',
'## How to Reschedule an Existing Appointment

ClinicDesk makes it easy to move an appointment to a new date, time, or provider without losing any existing notes or attachments.

## Rescheduling via the Calendar

1. Open the **Schedule** module from the left sidebar.
2. Locate the appointment on the calendar. Use the **Search** bar at the top of the calendar or navigate to the appointment''s current date.
3. Click on the appointment block to open the **Appointment Detail** panel.
4. Click the **Reschedule** button (calendar icon) at the top of the detail panel.
5. A reschedule dialog will appear. Select the new **Date**, **Time**, and optionally a different **Provider** or **Operatory**.
6. ClinicDesk will check availability in real time and flag any conflicts with a yellow warning banner.
7. Enter a **Reschedule Reason** from the dropdown (e.g., Patient Request, Provider Unavailable, Clinic Closure). This is logged in the appointment history.
8. Click **Confirm Reschedule** to save the changes.

## Rescheduling via Drag and Drop

- In the **Day** or **Week** calendar view, click and hold an appointment block.
- Drag it to the desired time slot and release.
- A confirmation dialog will appear summarizing the change. Click **Confirm** to apply.

## After Rescheduling

- The original appointment slot is freed automatically.
- If the patient had a pending reminder for the old appointment, it is cancelled and a new reminder is queued for the updated date/time.
- The **Appointment History** tab within the patient''s record will show a timestamped log of the reschedule, including which staff member made the change.

## Tips

- To reschedule multiple appointments at once (e.g., due to a provider absence), use **Bulk Reschedule** under **Schedule → Tools → Bulk Actions**.
- Patients can self-reschedule via the Patient Portal if that feature is enabled under **Settings → Patient Portal → Scheduling Permissions**.'),

('How to Cancel an Appointment and Manage the Waitlist',
'how-to-cancel-an-appointment-and-manage-the-waitlist',
'scheduling',
'## How to Cancel an Appointment and Manage the Waitlist

Cancelling appointments in ClinicDesk frees up slots immediately and allows you to offer that time to patients on the waitlist.

## Cancelling an Appointment

1. Navigate to the **Schedule** module and locate the appointment.
2. Click the appointment block to open the **Appointment Detail** panel.
3. Click the **Cancel Appointment** button (X icon) at the top of the panel.
4. Select a **Cancellation Reason** from the dropdown (e.g., Patient No-Show, Patient Request, Provider Emergency).
5. Choose whether to **Charge a Cancellation Fee** if your clinic has a policy configured under **Settings → Billing → Cancellation Policy**.
6. Click **Confirm Cancellation**. The slot will turn grey on the calendar to indicate it is open.

## Managing the Waitlist

The waitlist captures patients who want an earlier or alternative appointment time.

### Adding a Patient to the Waitlist
1. Go to **Schedule → Waitlist** in the top navigation bar.
2. Click **+ Add to Waitlist**.
3. Search for and select the patient.
4. Specify their preferred **Provider**, **Appointment Type**, and **Availability Windows** (e.g., mornings only, any weekday).
5. Click **Save**. The patient is now queued.

### Filling a Cancelled Slot from the Waitlist
1. After cancelling an appointment, ClinicDesk will automatically display a **Waitlist Match** banner listing patients whose preferences match the newly opened slot.
2. Click **Offer Slot** next to a patient''s name to send them an SMS or email with a link to confirm the time.
3. If the patient confirms, ClinicDesk books the appointment and removes them from the waitlist automatically.
4. If no response is received within the configured window (set under **Settings → Scheduling → Waitlist Timeout**), the next patient is offered the slot.

## Tips

- Filter the waitlist by provider, appointment type, or availability using the filter bar at the top of the Waitlist view.
- Waitlist history is retained on the patient''s profile under **Patient Record → Appointments → Waitlist History**.'),

('Setting Up Provider Schedules and Availability Blocks',
'setting-up-provider-schedules-and-availability-blocks',
'scheduling',
'## Setting Up Provider Schedules and Availability Blocks

Defining when each provider is available ensures that ClinicDesk only allows appointments to be booked during valid working hours.

## Accessing Provider Schedule Settings

1. Navigate to **Settings → Scheduling → Provider Schedules**.
2. Select the provider from the list on the left. All active providers in your clinic will appear here.

## Setting a Recurring Weekly Schedule

1. With the provider selected, click **Edit Schedule**.
2. For each day of the week, toggle the day **On** or **Off** using the switch.
3. For active days, set the **Start Time** and **End Time** using the time pickers.
4. If the provider takes a lunch break or has a mid-day gap, click **+ Add Break** and define the break window.
5. Click **Save Schedule**. These hours will repeat every week until modified.

## Adding Availability Blocks

Availability blocks override the standard schedule for specific dates (e.g., a provider working a half-day or covering an extra shift).

1. In the provider''s schedule view, click **+ Add Block** on the calendar.
2. Select the date and define the **Start Time** and **End Time** for the block.
3. Set the block type:
   - **Available** — marks time as bookable outside normal hours.
   - **Unavailable** — blocks time from receiving new bookings (e.g., staff meetings, CME).
   - **Out of Office** — indicates the provider is away; can trigger auto-reassignment rules.
4. Add an internal note describing the reason for the block.
5. Click **Save Block**.

## Copying Schedules Between Providers

- Use the **Copy Schedule** button to duplicate one provider''s weekly template to another. This is useful when onboarding new staff with similar hours.

## Tips

- Schedules must be saved before they take effect on the live calendar.
- Changes to a provider''s schedule do not affect already-booked appointments. ClinicDesk will flag any existing appointments that fall outside the new availability with an orange warning icon.
- Set clinic-wide holiday closures under **Settings → Scheduling → Clinic Hours & Holidays**.'),

('Managing Recurring Appointments',
'managing-recurring-appointments',
'scheduling',
'## Managing Recurring Appointments

ClinicDesk supports recurring appointment series for patients who need regular visits on a defined schedule, such as weekly therapy sessions or monthly hygiene recalls.

## Creating a Recurring Appointment

1. Open the **New Appointment** panel (click **+ New Appointment** or press Ctrl+N / Cmd+N).
2. Fill in the standard appointment details: patient, provider, appointment type, date, and time.
3. Toggle the **Recurring** switch to enable recurrence options.
4. Configure the recurrence pattern:
   - **Frequency**: Daily, Weekly, Bi-Weekly, Monthly, or Custom.
   - **Repeat Every**: Enter the interval (e.g., every 2 weeks).
   - **Day of Week**: Select which day(s) the appointment recurs.
   - **End Condition**: Choose **After X Occurrences** or **End by Date**.
5. ClinicDesk will display a preview list of all generated appointment dates. Review this list and remove any dates that fall on holidays or clinic closures.
6. Click **Save Series** to create all appointments at once.

## Editing a Recurring Series

1. Click on any appointment in the series to open the **Appointment Detail** panel.
2. Click **Edit**.
3. A dialog will ask: **Edit this appointment only** or **Edit all future appointments in this series**.
   - Choose **This Appointment** to make a one-time change.
   - Choose **This and Future Appointments** to update the remainder of the series.
4. Make your changes and click **Save**.

## Cancelling a Recurring Series

1. Open any appointment in the series.
2. Click **Cancel Appointment**.
3. When prompted, select **Cancel Entire Series** or **Cancel This Appointment Only**.

## Viewing All Appointments in a Series

- Open the patient''s record and go to **Appointments → Recurring Series** to see all past and upcoming appointments grouped by series.

## Tips

- Recurring appointments are colour-coded with a circular arrow icon on the calendar grid.
- If a provider is unavailable on a recurring date, ClinicDesk will flag that occurrence with a conflict warning rather than silently skipping it.'),

('Handling Double-Booking Conflicts',
'handling-double-booking-conflicts',
'scheduling',
'## Handling Double-Booking Conflicts

ClinicDesk has built-in conflict detection to prevent accidental double-bookings. This guide explains how conflicts are identified and how to resolve them.

## How ClinicDesk Detects Conflicts

When a new appointment is saved or an existing appointment is moved, ClinicDesk checks for:

- **Provider conflicts**: The same provider already has a booking at the overlapping time.
- **Operatory conflicts**: The same room or chair is assigned to two appointments at the same time.
- **Patient conflicts**: The same patient has two overlapping appointments on the same day.

If a conflict is detected, a red **Scheduling Conflict** banner appears at the top of the appointment panel and the Save button is disabled by default.

## Resolving a Provider Conflict

1. When the conflict banner appears, click **View Conflict Details** to see the overlapping appointment.
2. Options to resolve:
   - **Change the Time**: Adjust the start time so appointments no longer overlap.
   - **Change the Provider**: Reassign the new appointment to a different available provider by selecting from the **Provider** dropdown.
   - **Change the Operatory**: If the conflict is room-based only, select a different operatory.
3. Once the conflict is resolved, the banner disappears and the **Save Appointment** button becomes active.

## Enabling Override Mode (Admin Only)

In some clinics, double-booking is intentional (e.g., a provider seeing two patients in staggered rooms). Admins can enable override mode:

1. Navigate to **Settings → Scheduling → Conflict Rules**.
2. Toggle **Allow Double-Booking with Warning** to On.
3. Choose whether to require a **Justification Note** when overriding a conflict.
4. Click **Save**.

When override mode is on, staff can check **Override Conflict** on the appointment form and save the appointment with the conflict in place. A warning icon will appear on the calendar block.

## Reviewing Double-Booked Appointments

- Go to **Schedule → Reports → Conflict Report** to see a list of all current double-booked slots across all providers.

## Tips

- Conflicts are shown on the calendar as overlapping, striped appointment blocks for easy visual identification.
- Receive daily conflict summary emails by enabling them under **Settings → Notifications → Admin Alerts**.'),

('Setting Up Appointment Reminders (Email/SMS)',
'setting-up-appointment-reminders-email-sms',
'scheduling',
'## Setting Up Appointment Reminders (Email/SMS)

ClinicDesk can automatically send patients appointment reminders via email or SMS to reduce no-shows and last-minute cancellations.

## Accessing Reminder Settings

1. Navigate to **Settings → Scheduling → Appointment Reminders**.
2. The Reminders dashboard shows all active reminder rules and their delivery statistics.

## Creating a Reminder Rule

1. Click **+ Add Reminder Rule**.
2. Configure the following fields:
   - **Rule Name**: A descriptive label (e.g., "48-Hour SMS Reminder").
   - **Trigger**: How far in advance the reminder is sent. Enter a number and select Hours or Days (e.g., 48 hours before appointment).
   - **Channel**: Select **Email**, **SMS**, or **Both**.
   - **Applies To**: Choose whether this rule applies to all appointment types or select specific types from the dropdown.
3. Compose the reminder message:
   - For **Email**: Use the rich text editor. Insert dynamic fields like `{{patient_first_name}}`, `{{appointment_date}}`, `{{provider_name}}`, and `{{clinic_phone}}` using the **Insert Field** button.
   - For **SMS**: Keep the message under 160 characters. The same dynamic fields are available.
4. Toggle **Include Confirmation Link** to On if you want patients to confirm or cancel via a self-service link.
5. Click **Save Rule**.

## Managing Multiple Reminder Rules

You can stack multiple rules for a single appointment. A common setup is:

- 7 days before — Email reminder with preparation instructions.
- 48 hours before — SMS reminder with a confirmation link.
- 2 hours before — SMS reminder as a final notice.

Rules are evaluated and sent in order based on their trigger time.

## Patient Communication Preferences

- Individual patients can opt out of reminders in their profile under **Patient Record → Communication Preferences**.
- Patients who opt out will be shown with a muted bell icon on their appointment card.

## Reminder Delivery Logs

- View a full history of sent reminders under **Reports → Communication Logs**.
- Filter by date range, channel, status (Sent, Failed, Opened), and appointment type.

## Tips

- Test a reminder template by clicking **Send Test** on the rule editor before activating it.
- Ensure your clinic''s SMS sender ID and email domain are verified under **Settings → Integrations → Messaging**.'),

('Configuring Appointment Types and Durations',
'configuring-appointment-types-and-durations',
'scheduling',
'## Configuring Appointment Types and Durations

Appointment types define the nature of a visit and control default durations, colour coding, and billing codes in ClinicDesk.

## Accessing Appointment Type Settings

1. Navigate to **Settings → Scheduling → Appointment Types**.
2. A list of all existing appointment types is displayed, showing the name, default duration, colour, and active status.

## Creating a New Appointment Type

1. Click **+ New Appointment Type**.
2. Fill in the following fields:
   - **Name**: The label that appears on the calendar and in dropdowns (e.g., "New Patient Comprehensive Exam").
   - **Short Code**: An abbreviated label for tight calendar views (e.g., "NP EXAM").
   - **Default Duration**: Set in minutes (e.g., 60). This populates automatically when this type is selected during booking.
   - **Colour**: Choose a colour from the palette to visually distinguish this type on the calendar.
   - **Category**: Group the type under a category (e.g., Preventive, Restorative, Orthodontic, Emergency).
   - **Linked Procedure Codes**: Optionally attach one or more ADA or CPT codes that are pre-loaded onto the claim when this appointment type is used.
   - **Operatory Preference**: Assign a preferred operatory for this appointment type (e.g., all X-ray appointments default to Operatory 3).
   - **Instructions for Patient**: Add pre-visit instructions that are automatically included in reminder messages for this type.
3. Click **Save Appointment Type**.

## Editing an Existing Appointment Type

1. Click the pencil icon next to the appointment type in the list.
2. Make your changes and click **Save**.
3. Changes to duration will not retroactively affect already-booked appointments — only new bookings will use the updated default.

## Deactivating an Appointment Type

- Toggle the **Active** switch off to hide the type from booking dropdowns without deleting historical data.
- Deactivated types are shown in grey in the settings list and can be reactivated at any time.

## Tips

- Create separate appointment types for new vs. returning patients to capture the correct duration and billing codes automatically.
- Use the **Duplicate** button to create a variation of an existing type without starting from scratch.'),

('Viewing and Printing the Daily/Weekly Schedule',
'viewing-and-printing-the-daily-weekly-schedule',
'scheduling',
'## Viewing and Printing the Daily/Weekly Schedule

ClinicDesk offers flexible calendar views and print-ready schedule reports for front desk and clinical staff.

## Switching Calendar Views

1. Open the **Schedule** module from the left sidebar.
2. Use the view selector buttons in the top-right area of the calendar toolbar to switch between:
   - **Day View**: Shows a single day in a time-grid layout, with columns for each provider or operatory.
   - **Week View**: Shows a 5- or 7-day week with a condensed grid.
   - **Month View**: High-level overview with appointment counts per day.
   - **Agenda View**: A list-based view of upcoming appointments sorted by time.
3. Use the **< >** arrows or click **Today** to navigate between dates.

## Filtering the Calendar

- Click **Filter** in the toolbar to filter the calendar by:
  - **Provider**: Show one or multiple providers'' columns simultaneously.
  - **Appointment Type**: Hide or highlight specific appointment types.
  - **Operatory**: Show only appointments in selected rooms.
- Active filters are shown as blue tags in the toolbar. Click the X on any tag to remove it.

## Printing the Daily Schedule

1. Navigate to the date you want to print.
2. Click the **Print** button (printer icon) in the top-right of the calendar toolbar.
3. In the **Print Options** dialog, configure:
   - **View**: Day or Week.
   - **Providers**: Select which providers to include.
   - **Include Patient Details**: Toggle on to show patient DOB, phone number, and appointment notes on the printout.
   - **Include Open Slots**: Toggle on to print blank lines for unfilled time slots.
4. Click **Print** to send to your browser''s print dialog, or **Export PDF** to save a PDF file.

## Tips

- Bookmark specific filtered calendar views using the **Save View** button. Saved views appear in the **My Views** dropdown for quick access.
- The schedule auto-refreshes every 60 seconds.'),

('Managing Multiple Provider Calendars',
'managing-multiple-provider-calendars',
'scheduling',
'## Managing Multiple Provider Calendars

ClinicDesk allows you to view and manage appointments for all providers simultaneously or switch between individual provider calendars with ease.

## Viewing Multiple Provider Calendars Side by Side

1. Open the **Schedule** module.
2. In the **Day View**, each provider is displayed as a separate column. By default, all active providers for the selected date are shown.
3. To control which providers appear, click **Providers** in the toolbar.
4. Check or uncheck providers in the dropdown list. Changes apply instantly to the calendar grid.

## Assigning a Colour to Each Provider

1. Navigate to **Settings → Staff → Providers**.
2. Click the provider''s name to open their profile.
3. Under the **Calendar Settings** section, click the colour swatch next to **Calendar Colour** and choose a colour.
4. Click **Save**. The colour will appear on appointment blocks and column headers throughout the scheduler.

## Setting a Default Calendar View

1. Go to **Settings → Scheduling → Display Preferences**.
2. Under **Default Calendar View**, select which providers are shown by default when the Schedule module opens.
3. Choose the default view type (Day, Week, or Agenda) for each staff role.
4. Click **Save Preferences**.

## Switching to a Single Provider View

- Click a provider''s name in the column header to collapse the calendar to that provider only.
- Click **All Providers** in the toolbar to return to the multi-column view.

## Tips

- Use the **Agenda View** when coordinating across many providers — it shows a flat list of all appointments sorted by time, grouped by provider.
- Front desk staff can pin frequently managed provider columns using the **Pin Provider** option in the provider dropdown for faster daily access.')

ON CONFLICT (slug) DO NOTHING;

-- =============================================================================
-- BILLING & CODING (12 articles)
-- =============================================================================

INSERT INTO knowledge_articles (title, slug, category, content) VALUES

('Submitting a Claim to Insurance',
'submitting-a-claim-to-insurance',
'billing_coding',
'## Submitting a Claim to Insurance

ClinicDesk allows you to submit claims electronically or print paper claims directly from the patient''s account.

## Before You Begin

Ensure the following are complete before submitting:
- Patient insurance information is verified under **Patient Profile > Insurance Tab**
- All procedure codes and diagnosis codes are attached to the visit
- The rendering provider NPI is on file under **Settings > Providers**

## Steps to Submit a Single Claim

1. Navigate to **Billing > Claims Manager**.
2. Search for the patient using the top search bar and select the encounter date.
3. Review the claim summary on the right panel — confirm procedure codes, fees, and diagnosis codes are correct.
4. Click **Validate Claim** to run ClinicDesk''s built-in pre-submission checks. Resolve any red errors before proceeding.
5. Select the payer from the **Insurance** dropdown if multiple plans are on file.
6. Click **Submit Electronically** to transmit via your connected clearinghouse, or **Print CMS-1500 / ADA Claim Form** for paper submission.
7. The claim status will update to **Submitted** and a timestamp will appear in the **Claim History** panel.

## Claim Validation Errors

Common validation errors include:
- **Missing NPI**: Go to **Settings > Providers** and add the rendering provider''s 10-digit NPI.
- **Invalid diagnosis code**: Ensure ICD-10 codes are active for the date of service.
- **Duplicate claim warning**: ClinicDesk detects previously submitted claims for the same date and procedure. Review before resubmitting.

## Tips

- Enable automatic claim submission under **Settings > Billing Preferences > Auto-Submit on Checkout** to streamline your workflow.
- Use the **Claim Scrubber Report** under **Reports > Billing** to review common errors across your practice.'),

('Understanding CDT Codes (Dental)',
'understanding-cdt-codes-dental',
'billing_coding',
'## Understanding CDT Codes (Dental)

CDT (Current Dental Terminology) codes are maintained by the American Dental Association (ADA) and are required for all dental insurance claim submissions. ClinicDesk includes a built-in CDT code library updated annually.

## CDT Code Structure

Each CDT code begins with the letter **D** followed by four digits, grouped by category:
- **D0100–D0999** – Diagnostic (e.g., exams, X-rays)
- **D1000–D1999** – Preventive (e.g., cleanings, fluoride)
- **D2000–D2999** – Restorative (e.g., fillings, crowns)
- **D3000–D3999** – Endodontics (e.g., root canals)
- **D4000–D4999** – Periodontics (e.g., scaling and root planing)
- **D7000–D7999** – Oral and Maxillofacial Surgery (e.g., extractions)

## Commonly Used CDT Codes

| Code | Description |
|------|-------------|
| D0120 | Periodic oral evaluation |
| D0150 | Comprehensive oral evaluation |
| D0210 | Full mouth series of radiographic images |
| D0274 | Bitewing radiographic images – four images |
| D1110 | Prophylaxis – adult |
| D1120 | Prophylaxis – child |
| D2140 | Amalgam restoration – one surface, primary or permanent |
| D2750 | Crown – porcelain fused to high noble metal |
| D3310 | Endodontic therapy, anterior tooth |
| D4341 | Periodontal scaling and root planing – four or more teeth per quadrant |
| D7140 | Extraction, erupted tooth or exposed root |

## Tips

- Use the **Procedure Favorites** list under **Settings > Billing** to pin your most-used codes for faster charting.
- Attach a narrative to codes like D2750 or D4341 in the **Claim Notes** field when required by the payer.'),

('Understanding CPT Codes (Medical)',
'understanding-cpt-codes-medical',
'billing_coding',
'## Understanding CPT Codes (Medical)

CPT (Current Procedural Terminology) codes are maintained by the American Medical Association (AMA) and are used by medical clinics to report procedures and services to insurers.

## CPT Code Structure

CPT codes are five-digit numeric codes organized into three categories:
- **Category I** – Standard procedures and services (99000s for E&M, 10000s–69999 for surgery/diagnostics)
- **Category II** – Performance tracking codes (supplemental)
- **Category III** – Emerging technology codes

## Commonly Used CPT Codes

| Code | Description |
|------|-------------|
| 99213 | Office visit, established patient, low complexity |
| 99214 | Office visit, established patient, moderate complexity |
| 99203 | Office visit, new patient, low complexity |
| 99395 | Preventive visit, established patient, 18–39 years |
| 93000 | Electrocardiogram (ECG/EKG) |
| 85025 | Complete blood count (CBC) with differential |
| 71046 | Chest X-ray, two views |
| 36415 | Routine venipuncture |
| 90686 | Influenza vaccine, quadrivalent |
| 96372 | Therapeutic injection, subcutaneous or intramuscular |

## Using Modifiers

Add modifiers directly in the **Modifier** field next to the CPT code. Common modifiers include:
- **Modifier 25** – Significant, separately identifiable E&M on the same day as a procedure
- **Modifier 59** – Distinct procedural service
- **Modifier GT** – Telehealth services

## Tips

- Enable **Code Suggestions** under **Settings > Medical Billing** to have ClinicDesk recommend CPT codes based on your ICD-10 entries.'),

('Processing Patient Payments (Copays and Balances)',
'processing-patient-payments-copays-balances',
'billing_coding',
'## Processing Patient Payments (Copays and Balances)

ClinicDesk supports multiple payment methods for collecting patient responsibility amounts at checkout or from the patient ledger.

## Collecting a Copay at Checkout

1. When the appointment is marked as **Checked In**, a **Collect Copay** prompt will appear on the front desk screen.
2. Enter the copay amount (auto-populated if the patient''s insurance plan is configured).
3. Select the payment method:
   - **Credit/Debit Card** – Processed via the integrated card terminal
   - **Cash** – Enter the amount received; ClinicDesk will calculate change automatically
   - **Check** – Enter check number in the reference field
   - **Patient Portal / Online** – Displays a reference number if pre-paid online
4. Click **Post Payment** to apply the payment to the patient ledger.

## Applying a Payment to an Outstanding Balance

1. Go to **Billing > Patient Ledger** and search for the patient.
2. In the **Balance Due** column, click **Post Payment**.
3. Select the charges you wish to apply the payment to by checking the boxes next to each line item.
4. Enter the payment amount and method.
5. Click **Apply & Save**.

## Splitting Payments

To split a payment across multiple methods (e.g., $50 card + $20 cash):
1. Enter the first payment method and amount, then click **+ Add Another Payment Method**.
2. Repeat for each method.
3. Click **Post All Payments** when the total matches the amount due.

## Tips

- Enable **Copay Auto-Calculation** under **Settings > Insurance Plans** to pull copay amounts directly from the patient''s plan.
- Use the **End of Day Report** to reconcile daily payment totals.'),

('Setting Up Payment Plans',
'setting-up-payment-plans',
'billing_coding',
'## Setting Up Payment Plans

ClinicDesk allows you to create structured payment plans for patients with balances they cannot pay in full.

## Creating a Payment Plan

1. Go to **Billing > Patient Ledger** and open the patient''s account.
2. Click the **Payment Plans** tab, then click **+ New Payment Plan**.
3. Enter the following details:
   - **Plan Balance**: Total amount to be financed (auto-filled from balance due, editable)
   - **Down Payment**: Optional amount collected today
   - **Number of Installments**: Enter the number of monthly payments
   - **Start Date**: Date of first installment
   - **Payment Method on File**: Select a saved card or bank account, or click **Add New Method**
4. ClinicDesk will calculate the installment amount and display a **Plan Summary**. Confirm the amounts are correct.
5. Click **Save Payment Plan** to activate the plan.

## Auto-Charge for Installments

If a card or bank account is saved:
1. Toggle **Enable Auto-Charge** to ON in the plan settings.
2. ClinicDesk will automatically charge the payment method on the scheduled date and post the payment to the ledger.
3. The patient will receive an email receipt after each charge.

## Patient Communication

- ClinicDesk automatically sends a **Payment Plan Agreement** PDF to the patient''s email when the plan is created.
- Reminder emails are sent 3 days before each scheduled charge (configurable under **Settings > Notifications > Billing**).

## Tips

- Set a minimum balance threshold for auto-suggesting payment plans under **Settings > Billing Preferences > Payment Plans**.
- View all active payment plans under **Reports > Billing > Payment Plans Summary**.'),

('Generating and Sending Patient Invoices and Statements',
'generating-and-sending-patient-invoices-statements',
'billing_coding',
'## Generating and Sending Patient Invoices and Statements

ClinicDesk can generate individual invoices or batch patient statements to notify patients of their outstanding balances.

## Generating a Single Patient Invoice

1. Go to **Billing > Patient Ledger** and search for the patient.
2. Click **Generate Invoice** in the top-right toolbar.
3. In the invoice dialog:
   - Select the **Date Range** to include charges from a specific period.
   - Choose to include **Unapplied Credits** and **Insurance Pending** line items if desired.
   - Select the **Invoice Template** (Standard, Detailed, or Minimal).
4. Click **Preview** to review before sending.
5. Click **Send to Patient** to deliver via email, or **Print** for a paper copy.

## Batch Statement Generation

For sending statements to all patients with a balance:
1. Navigate to **Billing > Statements > Batch Statements**.
2. Set filters:
   - **Minimum Balance**: e.g., $5.00
   - **Balance Age**: e.g., show balances over 30 days
   - **Insurance Status**: Choose **Insurance Cleared** to exclude in-progress claims
3. Click **Preview Batch** to see the list of patients who will receive statements.
4. Click **Generate & Send All** to email all patients, or **Download PDF Bundle** to print and mail.

## Tips

- Schedule automatic monthly statements under **Settings > Billing Preferences > Auto-Statements** to run on the 1st of each month.'),

('Running End-of-Day Financial Reports',
'running-end-of-day-financial-reports',
'billing_coding',
'## Running End-of-Day Financial Reports

ClinicDesk''s End-of-Day (EOD) report summarizes all financial activity for the day, including payments collected, charges posted, and adjustments made.

## Accessing the End-of-Day Report

1. Navigate to **Reports > Financial > End of Day Report**.
2. The date defaults to today. To run for a past date, use the **Date Picker** to select the desired day.
3. Click **Generate Report**.

## Report Sections

### Payments Collected
- Totals by payment method: Cash, Credit/Debit, Check, Online
- Number of transactions per method

### Charges Posted
- Total charges entered for the day by procedure category

### Adjustments
- Insurance write-offs, courtesy discounts, and other adjustment types

### Claims Submitted
- Number of claims submitted electronically vs. paper
- Total billed amount

## Reconciling the Day

1. Compare the **Payments Collected** total to your physical drawer or card terminal batch totals.
2. Investigate any discrepancies by clicking **Drill Down** next to any line item to see individual transactions.
3. Once reconciled, click **Close Day** to lock the date and prevent backdated edits.

## Tips

- Enable the **Auto-Send EOD Report** under **Settings > Reports** to automatically email the report to designated staff at a set time each evening.'),

('Handling Refunds and Credits',
'handling-refunds-and-credits',
'billing_coding',
'## Handling Refunds and Credits

ClinicDesk supports issuing refunds to patients and applying unapplied credits to outstanding charges. All refund and credit activity is tracked in the patient ledger and audit log.

## Issuing a Refund to a Patient

1. Go to **Billing > Patient Ledger** and locate the patient''s account.
2. Confirm a credit balance is present (shown in green as a negative amount).
3. Click **Issue Refund** in the ledger toolbar.
4. Enter the refund amount (cannot exceed the available credit).
5. Select the refund method:
   - **Original Payment Method** – Reverses the card charge via ClinicDesk Payments
   - **Check** – Records a manual check refund; enter the check number
   - **Cash** – Records a cash refund
6. Add a note in the **Reason** field (e.g., "Patient overpaid at checkout 03/10/2026").
7. Click **Process Refund**. The ledger will update immediately.

## Applying a Credit to Future Charges

1. In the **Patient Ledger**, click **Apply Credit**.
2. Select the charge(s) to credit from the list of open balances.
3. Enter the credit amount to apply to each.
4. Click **Apply & Save**.

## Tips

- Managers can restrict refund permissions under **Settings > User Roles > Billing Permissions**.
- Run the **Credit Balances Report** under **Reports > Billing** monthly to identify and resolve outstanding credits.'),

('Managing Fee Schedules',
'managing-fee-schedules',
'billing_coding',
'## Managing Fee Schedules

Fee schedules in ClinicDesk define the amount billed for each procedure code. You can maintain multiple fee schedules for different insurance contracts, self-pay patients, and in-house membership plans.

## Accessing Fee Schedules

1. Navigate to **Settings > Billing > Fee Schedules**.
2. You will see a list of all fee schedules configured for your practice.

## Creating a New Fee Schedule

1. Click **+ New Fee Schedule**.
2. Enter a **Schedule Name** (e.g., "Delta Dental PPO 2026" or "Self-Pay Standard").
3. Select the **Type**: Insurance, Self-Pay, or Membership Plan.
4. Choose the **Code Type**: CDT (dental) or CPT (medical).
5. Click **Save** to create the schedule.

## Adding Fees

1. In the fee schedule editor, click **+ Add Code**.
2. Search for the procedure code (e.g., D1110 or 99213).
3. Enter the **Contracted Fee** and optionally the **UCR Fee**.
4. Click **Save Row**.
5. Or click **Import from CSV** to bulk-upload fees.

## Bulk Updating Fees

1. Click **Bulk Adjust** in the fee schedule toolbar.
2. Enter the percentage (e.g., 3% increase for annual UCR update).
3. Choose whether to round to the nearest dollar.
4. Click **Apply Adjustment**.

## Tips

- ClinicDesk will automatically use the assigned fee schedule when generating claims.
- Download the **Fee Schedule Comparison Report** under **Reports > Billing** to compare contracted rates against UCR fees.'),

('Understanding ERA and EOB Processing',
'understanding-era-eob-processing',
'billing_coding',
'## Understanding ERA and EOB Processing

An ERA (Electronic Remittance Advice) is the digital version of an EOB (Explanation of Benefits). ClinicDesk automatically retrieves ERAs from your clearinghouse and allows you to review and post payments with one click.

## Viewing Incoming ERAs

1. Navigate to **Billing > ERA / EOB Processing**.
2. The **Incoming ERAs** tab lists all unreviewed remittances. Each ERA shows payer name, check/EFT number, date of payment, total payment amount, and number of claims included.

## Auto-Posting an ERA

1. Click on an ERA to open the detail view.
2. Review the claim-by-claim breakdown — green rows indicate the paid amount matches the expected contractual amount.
3. Yellow rows indicate a discrepancy (e.g., partial payment or adjustment).
4. Click **Auto-Post** to apply all green-row payments automatically.
5. For yellow rows, review the adjustment reason code and decide:
   - **Accept Adjustment** – Posts the allowed amount and writes off the difference
   - **Post to Patient** – Applies the remainder to the patient''s balance
   - **Flag for Appeal** – Marks the claim for follow-up

## Common ERA Adjustment Reason Codes

| Code | Meaning |
|------|---------|
| CO-45 | Charge exceeds contracted rate |
| PR-1 | Applied to deductible |
| PR-2 | Applied to coinsurance |
| CO-4 | Service not covered |
| OA-23 | Payment adjusted due to information supplied |

## Tips

- Enable **ERA Auto-Post Rules** under **Settings > Billing > ERA Settings** to fully automate posting for specific payers where your contracted rates are consistent.'),

('Write-Off Procedures and Adjustments',
'write-off-procedures-and-adjustments',
'billing_coding',
'## Write-Off Procedures and Adjustments

Write-offs and adjustments in ClinicDesk allow you to reduce or eliminate a patient or insurance balance for legitimate reasons.

## Types of Adjustments

- **Contractual Write-Off**: The difference between your billed amount and the insurance allowed amount.
- **Courtesy Discount**: A discretionary reduction for staff, financial hardship, or goodwill.
- **Bad Debt Write-Off**: Applied when a balance is deemed uncollectible.
- **Small Balance Write-Off**: For balances below a defined threshold (e.g., under $5.00).
- **Insurance Adjustment**: Correction of an error in original charge entry.

## Posting a Write-Off on a Claim

1. Open the patient''s account under **Billing > Patient Ledger**.
2. Locate the charge line item and click **Adjust**.
3. In the **Post Adjustment** dialog:
   - Select the **Adjustment Type** from the dropdown
   - Enter the **Adjustment Amount**
   - Optionally enter a note in the **Reason** field
4. Click **Post Adjustment**. The balance will update immediately.

## Batch Small Balance Write-Off

1. Navigate to **Billing > Adjustments > Small Balance Write-Off Tool**.
2. Set the **Maximum Balance** threshold (e.g., $3.00).
3. Click **Preview** to see affected accounts.
4. Click **Apply Write-Offs** to process all at once.

## Tips

- Require manager approval for adjustments above a set dollar amount by enabling **Adjustment Approval Threshold** under **Settings > User Roles > Billing**.
- Always post contractual write-offs at the time of ERA processing to keep patient balances accurate.'),

('Batch Claim Submission',
'batch-claim-submission',
'billing_coding',
'## Batch Claim Submission

Batch claim submission allows you to submit multiple claims at once, saving time compared to submitting individually.

## Preparing Claims for Batch Submission

1. Go to **Billing > Claims Manager**.
2. Filter by **Status: Ready to Submit** and review the list.
3. Use the **Validate All** button to run pre-submission checks on all pending claims.

## Running an On-Demand Batch

1. In **Billing > Claims Manager**, filter by **Status: Ready to Submit**.
2. Select claims individually using the checkboxes, or click **Select All**.
3. Click **Submit Selected** in the toolbar.
4. In the confirmation dialog, review total number of claims, total billed amount, and payer breakdown.
5. Click **Confirm & Submit**. ClinicDesk will transmit the batch to your clearinghouse.

## Scheduling Automatic Batch Submission

1. Go to **Settings > Billing Preferences > Batch Submission**.
2. Toggle **Enable Scheduled Batches** to ON.
3. Set the submission time and days of the week.
4. Click **Save Schedule**.

## Handling Batch Rejections

1. Go to **Billing > Claims Manager** and filter by **Status: Rejected**.
2. Click the claim to view the rejection reason in the **Messages** tab.
3. Correct the issue and click **Resubmit Claim**.

## Tips

- Use the **Payer-Specific Rules** setting under **Settings > Insurance Plans** to automatically apply required modifiers before batch submission.
- Run the **Unbilled Encounters Report** under **Reports > Billing** daily to catch any charges that were not queued for submission.')

ON CONFLICT (slug) DO NOTHING;

-- =============================================================================
-- INSURANCE & CLAIMS (10 articles)
-- =============================================================================

INSERT INTO knowledge_articles (title, slug, category, content) VALUES

('Adding a New Insurance Plan for a Patient',
'adding-a-new-insurance-plan-for-a-patient',
'insurance_claims',
'## Adding a New Insurance Plan for a Patient

Use this guide to add or update a patient''s insurance coverage in ClinicDesk before scheduling or billing.

## Steps to Add an Insurance Plan

1. Open the patient''s chart by searching their name in the **Patient Search** bar at the top of any screen.
2. Click the **Insurance** tab on the left-side panel of the patient chart.
3. Click **+ Add Insurance Plan** in the upper-right corner.
4. In the **Carrier** field, begin typing the carrier name and select it from the dropdown.
5. Enter the **Member ID** exactly as shown on the insurance card, including any leading zeros or letter prefixes.
6. Enter the **Group Number** if applicable.
7. Fill in the **Subscriber Information** section:
   - If the patient is the subscriber, check **Patient is Subscriber**.
   - If the subscriber is someone else, enter their name, date of birth, and relationship to the patient.
8. Set the **Coverage Type**: choose **Primary**, **Secondary**, or **Tertiary**.
9. Enter the **Coverage Start Date**. If no end date is known, leave **Coverage End Date** blank.
10. Click **Save Insurance Plan**.

## Tips

- Always run an eligibility verification after adding a new plan.
- If the carrier is not listed in the dropdown, contact your ClinicDesk administrator to add it under **Settings > Insurance Carriers**.'),

('Verifying Insurance Eligibility',
'verifying-insurance-eligibility',
'insurance_claims',
'## Verifying Insurance Eligibility

ClinicDesk allows you to verify a patient''s insurance eligibility electronically in real time through our integrated clearinghouse connection.

## Electronic Eligibility Verification

1. Open the patient''s chart and click the **Insurance** tab.
2. Locate the insurance plan you want to verify and click the **Verify Eligibility** button (green checkmark icon).
3. Results typically return within 5–15 seconds. The status will update to:
   - **Active** — coverage is confirmed.
   - **Inactive** — coverage is not active as of today''s date.
   - **Unable to Verify** — the carrier did not return a response; verify manually.
4. Click **View Response** to see the full eligibility detail, including deductibles, annual maximums, copays, and coinsurance details.

## Batch Eligibility Verification

1. Go to **Billing > Eligibility > Batch Verification**.
2. Use the date filter to select tomorrow''s appointment date.
3. Click **Run Batch**. ClinicDesk will queue verification requests for all scheduled patients.

## Tips

- Re-verify eligibility at the start of each calendar year, as benefit limits reset annually.
- The last verification date and result are displayed in the **Last Verified** column of the Insurance tab.'),

('Submitting Pre-Authorizations and Prior Approvals',
'submitting-pre-authorizations-and-prior-approvals',
'insurance_claims',
'## Submitting Pre-Authorizations and Prior Approvals

Some procedures require prior authorization from the insurance carrier before treatment can be rendered.

## Submitting an Electronic Pre-Authorization

1. Go to **Billing > Pre-Authorizations > New Request**.
2. Select the **Patient** and confirm their active primary insurance plan.
3. Add one or more procedure codes using the **+ Add Procedure** button.
4. Attach supporting documentation if required: click **Attach Documents** to upload X-rays, photos, or clinical notes.
5. Enter the **Treating Provider** and **Service Facility** if different from the primary location.
6. Click **Submit Pre-Authorization**. ClinicDesk will transmit the request electronically via the clearinghouse.

## Tracking Pre-Authorization Status

- Navigate to **Billing > Pre-Authorizations** to view all open requests.
- Status values include: **Submitted**, **Approved**, **Denied**, **Pending Additional Info**, and **Expired**.
- When approved, ClinicDesk will display the **Authorization Number** and **Authorized Units**.

## Tips

- Pre-authorization approval does not guarantee payment — it only confirms medical necessity.
- Approvals typically expire after 90–180 days. Watch the **Expiration Date** column.
- Always reference the authorization number when submitting the final claim.'),

('Handling Denied Claims — Common Denial Codes and Resolutions',
'handling-denied-claims-common-denial-codes-and-resolutions',
'insurance_claims',
'## Handling Denied Claims — Common Denial Codes and Resolutions

When a claim is denied, ClinicDesk displays the denial reason code on the ERA. Use this guide to interpret common codes and take corrective action.

## Common Denial Codes and Resolutions

### CO-4 — Service Not Covered / Inconsistent with Modifier
- **Meaning:** The procedure code and modifier combination is invalid for this payer.
- **Resolution:** Review the modifier applied. Correct it and resubmit via **Actions > Correct and Resubmit**.

### CO-16 — Claim Lacks Information / Submission Errors
- **Meaning:** Required fields are missing or invalid (e.g., NPI, date of service, diagnosis code).
- **Resolution:** Open the claim, click **Edit Claim**, and verify all required fields.

### CO-97 — Payment Included in Previous Allowance
- **Meaning:** The procedure was already paid as part of a bundled service.
- **Resolution:** Review the original claim to confirm bundling. If bundling was incorrect, appeal with documentation.

### PR-1 — Deductible Amount
- **Meaning:** The denial represents the patient''s deductible responsibility.
- **Resolution:** No resubmission needed. Post the amount as **Patient Responsibility** and generate a patient statement.

### CO-29 — Claim Expired / Timely Filing
- **Meaning:** The claim was submitted after the carrier''s timely filing deadline.
- **Resolution:** File an appeal with proof of original timely submission.

### CO-50 — Procedure Not Deemed Medically Necessary
- **Meaning:** The carrier does not consider the service medically necessary.
- **Resolution:** Appeal with clinical notes, X-rays, and a letter of medical necessity.

## Tips

- Set up **Denial Alerts** under **Settings > Notifications** to receive email alerts when a claim is denied.
- Track denial trends by running the **Denial Analysis Report** under **Reports > Billing Reports**.'),

('Filing Insurance Appeals',
'filing-insurance-appeals',
'insurance_claims',
'## Filing Insurance Appeals

If a claim has been denied and you believe the denial is incorrect, ClinicDesk provides a structured workflow for filing formal appeals.

## Initiating an Appeal

1. Go to **Billing > Claims** and locate the denied claim.
2. Click the claim to open the **Claim Detail** view.
3. Click **Actions > File Appeal**.

## Completing the Appeal

1. In the **Appeal Reason** field, describe the basis for your appeal clearly and concisely.
2. Select the **Appeal Type**: First Level, Second Level, or External Review.
3. Attach supporting documentation: clinical notes, X-rays, prior authorization approvals, proof of timely filing, or a letter of medical necessity.
4. Confirm the **Appeal Deadline**. Most carriers require first-level appeals within 60–180 days of the denial date.
5. Click **Submit Appeal**.

## Tracking Appeal Status

- Navigate to **Billing > Appeals** to see all open appeals.
- Status values: **Submitted**, **In Review**, **Upheld** (denial stands), **Overturned** (payment approved), **Escalated**.
- ClinicDesk sends an automatic reminder if an appeal has been open for more than 30 days without a response.

## Tips

- Keep appeal language factual and reference specific policy provisions or EOB codes.
- Save carrier-specific appeal address information under **Settings > Insurance Carriers > [Carrier Name] > Appeal Address**.'),

('Coordination of Benefits — Primary vs Secondary Insurance',
'coordination-of-benefits-primary-vs-secondary-insurance',
'insurance_claims',
'## Coordination of Benefits — Primary vs Secondary Insurance

Coordination of Benefits (COB) applies when a patient is covered by more than one insurance plan.

## Setting Up COB in ClinicDesk

1. Open the patient chart and click the **Insurance** tab.
2. Confirm the patient has at least two active insurance plans listed.
3. Verify the **Coverage Type** for each plan: the plan that pays first must be **Primary**, the plan that pays second must be **Secondary**.

## Determining Which Plan is Primary

- **Birthday Rule (for dependents):** The plan of the parent whose birthday falls earlier in the calendar year is primary.
- **Active vs Retirement Coverage:** Active employer coverage is typically primary over Medicare or retirement coverage.
- **COBRA:** COBRA coverage is usually secondary to active group coverage.

## Submitting a COB Claim

1. Submit the claim to the **Primary** carrier first.
2. Once the primary EOB is received and posted, ClinicDesk will display a **Submit to Secondary** prompt.
3. Click **Submit to Secondary**. ClinicDesk will automatically populate the secondary claim with the primary carrier''s paid amount and adjustment codes.
4. Any remaining balance after both carriers have paid becomes patient responsibility.

## Tips

- Always confirm COB order at least once per year and when a patient reports a change in coverage.
- Run the **COB Aging Report** under **Reports > Billing Reports** to identify claims waiting for secondary submission.'),

('Understanding Insurance Fee Schedules vs Office Fee Schedules',
'understanding-insurance-fee-schedules-vs-office-fee-schedules',
'insurance_claims',
'## Understanding Insurance Fee Schedules vs Office Fee Schedules

ClinicDesk maintains two types of fee schedules: the **Office Fee Schedule** (your standard charges) and **Insurance Fee Schedules** (contracted rates for specific carriers).

## Office Fee Schedule

Contains the full fees your practice charges for each procedure code. View or edit under **Settings > Fee Schedules > Office Fee Schedule**.

## Insurance Fee Schedules

Reflect the contracted (allowed) amounts for each procedure code with a specific carrier. View under **Settings > Fee Schedules > Insurance Fee Schedules**, then select the carrier.

## How ClinicDesk Applies Fee Schedules

1. ClinicDesk uses the **Office Fee** as the billed amount on the claim.
2. When an ERA is received, ClinicDesk compares the carrier''s **Allowed Amount** to the office fee.
3. The difference is automatically posted as a **Contractual Adjustment**.
4. The remaining balance is posted as **Patient Responsibility**.

## Tips

- If no insurance fee schedule is linked, ClinicDesk will not auto-calculate write-offs.
- Run the **Fee Schedule Variance Report** under **Reports > Financial Reports** to identify procedures where your office fee significantly exceeds the allowed amount.'),

('Tracking Outstanding Claims — Aging Reports',
'tracking-outstanding-claims-aging-reports',
'insurance_claims',
'## Tracking Outstanding Claims — Aging Reports

The Insurance Aging Report gives you a real-time view of all claims that have been submitted but not yet paid.

## Running the Insurance Aging Report

1. Go to **Reports > Billing Reports > Insurance Aging**.
2. Configure filters: Date Range, Carrier, Provider, Location.
3. Click **Run Report**.

## Understanding the Aging Buckets

| Bucket | Days Since Submission |
|---|---|
| Current | 0–30 days |
| 31–60 days | 31–60 days |
| 61–90 days | 61–90 days |
| 91–120 days | 91–120 days |
| 120+ days | Over 120 days |

Claims in the **91–120** and **120+** buckets require immediate follow-up.

## Following Up on Outstanding Claims

1. Click on any claim to open the **Claim Detail** view.
2. Click **Actions > Check Claim Status** to query the clearinghouse for a real-time status update.
3. To initiate a phone follow-up, click **Actions > Log Follow-Up Call** and record the outcome.

## Tips

- Aim to work your aging report at minimum once per week.
- Export the report to CSV or PDF by clicking the **Export** button.'),

('Common Pre-Authorization Errors and Fixes',
'common-pre-authorization-errors-and-fixes',
'insurance_claims',
'## Common Pre-Authorization Errors and Fixes

Pre-authorization requests are sometimes rejected or returned with errors. This guide covers the most common errors and how to resolve them.

### Missing or Invalid NPI
- **Message:** "Rendering provider NPI is required" or "NPI not found in NPPES registry."
- **Fix:** Go to **Settings > Providers**, select the provider, and verify the NPI under the **Credentials** tab.

### Invalid Procedure Code
- **Message:** "Procedure code D6010 is not valid for this carrier."
- **Fix:** Verify the code in the **Code Library** under **Settings > Procedure Codes**. Check with the carrier for alternative accepted codes.

### Duplicate Pre-Authorization Request
- **Message:** "A pre-authorization for this procedure already exists for this member."
- **Fix:** Check **Billing > Pre-Authorizations** for an existing approved or pending auth.

### Missing Attachment / Supporting Documentation
- **Message:** "X-ray or clinical documentation is required for this procedure."
- **Fix:** Return to the pre-auth, click **Edit**, then **Attach Documents**. Upload the required files and click **Resubmit**.

### Patient Not Found / Member ID Mismatch
- **Message:** "Member ID not found" or "Patient date of birth does not match carrier records."
- **Fix:** Contact the patient to confirm current insurance information. Update the insurance plan on the patient chart and resubmit.

## Tips

- Resolve pre-auth errors before scheduling the associated procedure to avoid claim denials later.'),

('Updating Insurance Information When a Patient Changes Plans',
'updating-insurance-information-when-a-patient-changes-plans',
'insurance_claims',
'## Updating Insurance Information When a Patient Changes Plans

When a patient reports a change in insurance, it is important to update ClinicDesk promptly to avoid claim rejections.

## Step 1 — Collect Updated Information

Collect the new insurance card (front and back), carrier name, Member ID, Group Number, subscriber information, and coverage effective date.

## Step 2 — Inactivate the Old Plan

1. Open the patient chart and click the **Insurance** tab.
2. Locate the old insurance plan and click **Edit**.
3. Set the **Coverage End Date** to the last day the old plan was active.
4. Click **Save**. Do not delete the old plan — it must remain for historical claim reference.

## Step 3 — Add the New Plan

1. Click **+ Add Insurance Plan**.
2. Enter all details for the new plan.
3. Set the **Coverage Start Date** and **Coverage Type** (Primary or Secondary).
4. Click **Save Insurance Plan**.

## Step 4 — Verify Eligibility

Click **Verify Eligibility** next to the new plan and confirm it is active.

## Step 5 — Review Open Claims

1. Go to **Billing > Claims** and filter by the patient''s name to identify any pending claims.
2. For claims where the date of service falls under the new plan, update the insurance assignment and resubmit.

## Tips

- Run an eligibility check immediately after adding the new plan.
- Update the insurance change in ClinicDesk the same day the patient reports it.')

ON CONFLICT (slug) DO NOTHING;

-- =============================================================================
-- PATIENT RECORDS (9 articles)
-- =============================================================================

INSERT INTO knowledge_articles (title, slug, category, content) VALUES

('Creating a New Patient Record',
'creating-a-new-patient-record',
'patient_records',
'## Creating a New Patient Record

Adding a new patient to ClinicDesk takes just a few minutes.

## Getting Started

Navigate to **Patients** in the left sidebar, then click the **+ New Patient** button in the upper-right corner.

## Required Fields

- **First Name** and **Last Name**
- **Date of Birth**
- **Primary Phone Number**
- **Sex at Birth**

## Step-by-Step Instructions

1. Enter the patient''s legal first and last name. Use the **Preferred Name** field if the patient goes by a different name.
2. Select the **Date of Birth** using the calendar picker or type in MM/DD/YYYY format.
3. Enter at least one phone number. Mark the preferred contact method using the star icon.
4. Add the patient''s email address to enable appointment reminders and portal access.
5. Enter the home address in the **Address** section.
6. Under **Insurance**, click **Add Insurance Plan** to attach primary coverage.
7. Assign a **Primary Provider** and **Primary Location** from the dropdowns.
8. Click **Save Patient** to create the record.

## After Saving

You can upload a photo ID or insurance card under the **Documents** tab, complete the medical history form under **Health History**, and schedule the first appointment.

## Tips

- Use the **Duplicate Check** prompt that appears if a matching name and date of birth already exist.
- Fields marked with a red asterisk are required.'),

('Updating Patient Demographics',
'updating-patient-demographics',
'patient_records',
'## Updating Patient Demographics

Keeping patient demographic information current ensures accurate billing, proper communication, and regulatory compliance.

## Accessing the Demographics Tab

1. Open the patient''s profile by searching their name in the **Global Search** bar.
2. Click the patient''s name to open their profile.
3. Select the **Demographics** tab.

## Making Changes

1. Click the **Edit** button (pencil icon) in the top-right corner.
2. Modify the relevant fields (name, address, phone, email, emergency contact, etc.).
3. If updating an address, use the **Verify Address** button to validate it against USPS records.
4. Click **Save Changes**.

## Tracking Changes

ClinicDesk logs all demographic updates automatically under the **Activity Log** tab on the patient profile.

## Tips

- Always confirm the patient''s address and phone number at each visit check-in.
- Changes to legal name require a note in the **Reason for Change** field for audit purposes.'),

('Managing Patient Documents and Attachments',
'managing-patient-documents-and-attachments',
'patient_records',
'## Managing Patient Documents and Attachments

ClinicDesk allows you to store, organize, and retrieve patient documents directly within the patient record. Supported file types include PDF, JPEG, PNG, TIFF, DOCX, and XLSX.

## Uploading a New Document

1. Open the patient''s profile and click the **Documents** tab.
2. Click **Upload Document** in the upper-right corner.
3. Select the file from your computer or drag and drop it into the upload window.
4. Choose a **Document Category**: Insurance Card, Photo ID, Referral Letter, Lab Result, Consent Form, or Other.
5. Enter an optional **Document Name** and **Notes**.
6. Click **Upload**.

## Viewing and Downloading

- Click the document name to open a preview in the built-in document viewer.
- Use the **Download** button to save a copy locally.

## Deleting Documents

Documents can only be deleted by staff with the **Documents: Delete** permission. Deleted documents are moved to the archive for 90 days before permanent removal.

## Storage Limits

Each patient record supports up to 500 MB of attachments.'),

('HIPAA-Compliant Record Handling in ClinicDesk',
'hipaa-compliant-record-handling',
'patient_records',
'## HIPAA-Compliant Record Handling in ClinicDesk

ClinicDesk is designed to support your clinic''s HIPAA compliance obligations.

## Access Controls

ClinicDesk uses role-based access control (RBAC). Assign staff roles under **Settings > Staff > Roles & Permissions** with granular permissions for viewing, editing, printing, and exporting patient data.

## Audit Logging

All access to patient records is automatically logged, capturing user name, date/time, actions performed, and IP address. Review audit logs at **Reports > Compliance > Audit Log**.

## Data Encryption

- All data is encrypted in transit using TLS 1.2 or higher.
- Data at rest is encrypted using AES-256.
- Backups are encrypted and stored in geo-redundant data centers.

## Automatic Session Timeout

ClinicDesk automatically logs out inactive sessions after the timeout period set under **Settings > Security > Session Timeout** (default: 15 minutes).

## Breach Response

If you suspect unauthorized access to PHI, immediately contact your Privacy Officer and refer to **Settings > Compliance > Breach Notification Workflow**.

## Business Associate Agreement

Download your BAA at any time from **Settings > Compliance > Business Associate Agreement**.'),

('Merging Duplicate Patient Records',
'merging-duplicate-patient-records',
'patient_records',
'## Merging Duplicate Patient Records

Duplicate patient records can cause billing errors and fragmented medical histories. ClinicDesk provides a guided merge tool to consolidate duplicates safely.

## Finding Duplicates

1. Go to **Patients > Duplicate Management**.
2. Review pairs of records with a match confidence score (High, Medium, Low).
3. Click **Review** next to any pair to begin the merge process.

## Performing the Merge

1. In the **Merge Patients** screen, the left column shows the **Source** record and the right shows the **Target** (primary record to keep).
2. For each field where the two records differ, select which value to retain.
3. Click **Preview Merge** to review all changes.
4. Click **Confirm Merge**.

## After the Merge

- The source record is deactivated and marked as **Merged** — it is not deleted.
- All appointments, notes, documents, and billing history are transferred to the target record.
- Future searches for the source record''s name will redirect to the target record.

## Undoing a Merge

Merges can be reversed within 30 days by navigating to **Patients > Duplicate Management > Merge History** and clicking **Undo Merge**.'),

('Patient Intake Form Setup (Digital vs Paper)',
'patient-intake-form-setup',
'patient_records',
'## Patient Intake Form Setup (Digital vs Paper)

ClinicDesk supports both digital and paper-based patient intake workflows.

## Digital Intake Forms

### Setting Up a Digital Intake Form

1. Navigate to **Settings > Forms & Templates > Intake Forms**.
2. Click **+ New Form** or select an existing template.
3. Use the drag-and-drop form builder to add fields: text inputs, dropdowns, date pickers, signature fields, medical history checklists.
4. Under **Form Settings**, configure trigger (auto-send on new appointment), delivery method (email, SMS, or both), and deadline.
5. Click **Publish Form**.

### Sending Manually

1. Open the patient''s profile.
2. Click **Actions > Send Intake Form**.
3. Select the form and delivery method.
4. Click **Send Now**.

## Paper Intake Forms

1. Go to **Settings > Forms & Templates > Intake Forms**.
2. Click the **Print** icon to download a formatted PDF.
3. After the patient completes the form, scan it and upload to the patient''s **Documents** tab.

## Tips

- Send digital intake forms at least 24 hours before the appointment.
- A green checkmark in the **Appointments** view indicates the form has been submitted.'),

('Viewing Patient History and Treatment Notes',
'viewing-patient-history-and-treatment-notes',
'patient_records',
'## Viewing Patient History and Treatment Notes

ClinicDesk consolidates a patient''s full clinical history in one place.

## Accessing Patient History

1. Open the patient''s profile from **Patients > Patient List** or via **Global Search**.
2. Click the **Clinical** tab.
3. Use sub-tabs: **Visit History**, **Treatment Notes**, **Health History**, **Diagnoses & Conditions**, **Medications**, **Allergies**.

## Reading Treatment Notes

Notes appear in reverse chronological order. Each note displays visit date, provider name, chief complaint, treatment performed, and follow-up instructions.

## Filtering and Searching

Use the **Filter** panel to narrow results by date range, provider, appointment type, or diagnosis code. Use the **Search within notes** bar to find specific keywords.

## Adding a Treatment Note

1. Open the appointment from the **Calendar** or patient''s **Visit History**.
2. Click **Add Note**.
3. Select a note template or use the free-text editor.
4. Click **Sign & Save** to finalize. Signed notes cannot be edited — use **Addendum** to append corrections.

## Tips

- Click **Export Clinical Summary** to generate a C-CDA-compliant document for care coordination and referrals.'),

('Archiving Inactive Patient Records',
'archiving-inactive-patient-records',
'patient_records',
'## Archiving Inactive Patient Records

Archiving keeps your active patient list manageable while preserving historical records.

## When to Archive

- Patient has not had an appointment in 3+ years with no pending treatment
- Patient has transferred to another practice
- Patient is deceased

Do not archive patients with outstanding balances, pending claims, or scheduled appointments.

## Archiving a Single Patient

1. Open the patient''s profile.
2. Click **Actions > Archive Patient**.
3. Choose an **Archive Reason** and add an optional note.
4. Click **Confirm Archive**.

## Archiving Multiple Patients

1. Go to **Patients > Patient List**.
2. Click **Filters** and set **Last Visit** to **More than 3 years ago** and **Balance** to **$0.00**.
3. Select patients and click **Bulk Actions > Archive Selected**.

## Accessing Archived Records

Go to **Patients > Patient List**, then click **Filters > Status > Archived**. All history remains intact.

## Reactivating

Open the archived profile and click **Actions > Reactivate Patient**.'),

('Exporting Patient Data',
'exporting-patient-data',
'patient_records',
'## Exporting Patient Data

ClinicDesk allows authorized staff to export patient data for care coordination, patient requests, audits, and practice transitions.

## Clinical Summary Export

1. Open the patient''s profile and navigate to the **Clinical** tab.
2. Click **Export Clinical Summary**.
3. Choose format: **PDF** (human-readable) or **C-CDA XML** (for EHR transfers).
4. Select the date range and click **Generate Export**.

## Full Record Export

1. Open the patient''s profile.
2. Click **Actions > Export Full Record**.
3. Select data types to include: Demographics, Clinical notes, Documents, Billing history, Appointment history.
4. Choose output format (PDF or ZIP archive).
5. Click **Export**.

## Bulk Patient Export

1. Navigate to **Reports > Data Export > Bulk Patient Export**.
2. Apply filters to select the patient population.
3. Click **Request Export**. You''ll receive an email notification when ready.

## Audit Trail

Every export generates an entry in the **Audit Log** at **Reports > Compliance > Audit Log**.

## Tips

- Complete patient data requests under HIPAA''s Right of Access within 30 days.')

ON CONFLICT (slug) DO NOTHING;

-- =============================================================================
-- REPORTING & ANALYTICS (8 articles)
-- =============================================================================

INSERT INTO knowledge_articles (title, slug, category, content) VALUES

('Running Daily Production Reports',
'running-daily-production-reports',
'reporting_analytics',
'## Running Daily Production Reports

Daily production reports give you a snapshot of your clinic''s financial activity for any given day.

## Accessing the Report

1. Navigate to **Reports** in the top navigation bar.
2. Select **Financial Reports** from the dropdown menu.
3. Click **Daily Production Summary**.

## Setting Your Parameters

- **Date Range**: Set both dates to the same day for a single-day report.
- **Provider Filter**: Leave set to **All Providers** or select a specific provider.
- **Include Adjustments**: Check this box to include write-offs and courtesy discounts.

## Reading the Report

- **Gross Production**: Total charges before adjustments.
- **Adjustments**: Insurance write-offs, courtesy discounts, and manual adjustments.
- **Net Production**: Gross production minus all adjustments.
- **Collections**: Payments received (insurance and patient).

## Tips

- Run this report at the end of each business day before closing out.
- Click **Export** to save the report as PDF or CSV.
- Schedule automatic email delivery under **Schedule Report** at the top of the report screen.'),

('Running Accounts Receivable Aging Reports',
'running-accounts-receivable-aging-reports',
'reporting_analytics',
'## Running Accounts Receivable Aging Reports

The AR Aging Report shows outstanding balances grouped by how long they have been unpaid.

## Accessing the Report

1. Go to **Reports** in the top navigation bar.
2. Click **Financial Reports**, then select **AR Aging**.

## Configuring the Report

- **AR Type**: Choose **Insurance AR**, **Patient AR**, or **Combined**.
- **Aging Buckets**: ClinicDesk defaults to 0–30, 31–60, 61–90, and 90+ days. Customizable under **Settings > Report Defaults**.
- **Grouping**: Group by **Provider**, **Insurance Carrier**, or **Patient**.

## Interpreting the Results

- **Current (0–30 days)**: Recently billed, within normal turnaround.
- **31–60 Days**: Flag for follow-up.
- **61–90 Days**: Requires active follow-up.
- **90+ Days**: High risk of write-off. Evaluate for collections escalation.

## Tips

- Run the report weekly, every Monday morning.
- Sort by the **90+ Days** column descending to prioritize the oldest balances.
- Click any balance amount to drill into the individual claims.'),

('Running Provider Productivity Reports',
'running-provider-productivity-reports',
'reporting_analytics',
'## Running Provider Productivity Reports

Provider productivity reports evaluate individual provider performance based on production, collections, and patient volume.

## Accessing the Report

1. Click **Reports** in the navigation bar.
2. Select **Provider Reports**, then **Provider Productivity Summary**.

## Metrics Displayed

- **Appointments Seen**: Total completed visits.
- **Gross Production**: Total charges generated.
- **Net Production**: Charges after adjustments.
- **Collections**: Payments collected attributable to the provider.
- **Collection Rate**: Collections divided by net production, as a percentage.
- **Avg Production per Visit**: Net production divided by appointments seen.

## Benchmarking

Click **Show Benchmarks** to overlay industry averages by practice type (General Dentistry, Specialty, or Medical).

## Tips

- Click on any provider''s name to see a detailed breakdown by procedure code category, day of week, and insurance carrier.'),

('Custom Report Builder Overview',
'custom-report-builder-overview',
'reporting_analytics',
'## Custom Report Builder Overview

The Custom Report Builder lets you construct reports tailored to your practice''s specific needs.

## Accessing the Builder

1. Navigate to **Reports** in the top navigation bar.
2. Click **Custom Report Builder** at the bottom of the left panel.

## Step 1: Choose a Data Source

Select from: Appointments, Charges & Payments, Patients, Insurance Claims, or Providers. Join multiple data sources by clicking **Add Related Data**.

## Step 2: Select Fields

Drag fields from the **Available Fields** panel into the **Report Columns** area. Each field can be sorted, filtered, and aggregated (sum, count, average).

## Step 3: Apply Filters

Click **Add Filter** to restrict results. Supports equals, contains, starts with, date ranges, and multi-value selection.

## Step 4: Preview and Save

Click **Preview** to see up to 100 rows. Click **Save Report** and optionally assign to a folder.

## Sharing Reports

Open a saved report and click **Share**. Select individual users or roles and set permission to **View** or **Edit**.'),

('Exporting Reports to CSV and PDF',
'exporting-reports-to-csv-pdf',
'reporting_analytics',
'## Exporting Reports to CSV and PDF

ClinicDesk supports exporting any standard or custom report to CSV or PDF.

## Exporting to CSV

1. Open any report and apply your desired filters.
2. Click **Export** in the upper-right corner.
3. Select **CSV (.csv)** and choose **Current View** or **Full Data**.
4. Click **Download**.

## Exporting to PDF

1. Open the report and click **Export**, then **PDF (.pdf)**.
2. Configure orientation (Portrait/Landscape), paper size, and header options.
3. Click **Generate PDF**.

## Bulk Export

1. Go to **Reports > Report Library**.
2. Check the boxes next to reports you want to export.
3. Click **Bulk Export** and choose your format. ClinicDesk will package them into a ZIP file.

## Tips

- Any report can be scheduled for automatic delivery via email in CSV or PDF format.'),

('Understanding the Dashboard Metrics',
'understanding-the-dashboard-metrics',
'reporting_analytics',
'## Understanding the Dashboard Metrics

The ClinicDesk Dashboard provides a real-time overview of your practice''s key performance indicators.

## Default Dashboard Widgets

### Today''s Overview
- **Scheduled Appointments**: Total visits today.
- **Confirmed Appointments**: Count of confirmed patients.
- **Patients Checked In**: Live count updated in real time.
- **Daily Production (MTD)**: Running total of net production for the current month.

### Collections Snapshot
- **Today''s Payments**: Total payments posted today.
- **Month-to-Date Collections**: Total collected since the 1st.
- **Collection Rate (MTD)**: Percentage of net production collected.

### Outstanding AR Summary
A color-coded bar showing balance distribution by aging bucket.

## Customizing Your Dashboard

1. Click **Customize Dashboard** in the top-right corner.
2. Drag widgets from the **Available Widgets** panel.
3. Resize widgets by dragging the bottom-right corner handle.
4. Click **Save Layout**.

## Tips

- Each user can save a personal layout. Role-based defaults are configured under **Settings > Dashboard Defaults**.
- Dashboard data updates automatically every 5 minutes.'),

('End-of-Month and End-of-Year Reporting Procedures',
'end-of-month-and-end-of-year-reporting-procedures',
'reporting_analytics',
'## End-of-Month and End-of-Year Reporting Procedures

Closing out a month or year involves running a standard set of reports to reconcile activity.

## End-of-Month Checklist

1. **Post all pending transactions**: Confirm under **Billing > Unposted Transactions**.
2. **Run Monthly Production Summary**: **Reports > Financial Reports > Monthly Production Summary**.
3. **Run Monthly Collections Report**: Verify totals match bank deposits.
4. **Review AR Aging Report**: Identify balances that moved into 60+ or 90+ day buckets.
5. **Reconcile Insurance Payments**: Run **Reports > Insurance Reports > ERA Reconciliation**.
6. **Export and Archive**: Save all reports to PDF.
7. **Lock the Period**: Go to **Settings > Period Management** and click **Lock Month**.

## End-of-Year Checklist

In addition to month-end:
- Run the **Annual Production Report**.
- Run the **Provider Year-End Report**.
- Generate **1099 and Tax Summary Reports** under **Reports > Tax & Compliance**.
- Archive all reports and confirm backups.

## Tips

- Locked periods can be unlocked by administrators under **Settings > Period Management > Unlock Period** with a logged reason.'),

('Insurance Collections vs Patient Collections Reports',
'insurance-collections-vs-patient-collections-reports',
'reporting_analytics',
'## Insurance Collections vs. Patient Collections Reports

Understanding the split between insurance and patient payments is essential for tracking revenue mix and billing effectiveness.

## Accessing the Report

Go to **Reports > Financial Reports > Collections by Payer Type**.

## Report Sections

### Insurance Collections
- Primary and secondary insurance payments
- Electronic Remittances (ERAs) vs manual check payments
- Contractual adjustments

### Patient Collections
- Copays collected at check-in
- Balance payments
- Payment plan installments
- Online payments from the Patient Portal

### Combined View
Toggle to **Combined View** to see both streams side by side with percentage split.

## Filtering Options

- Date Range, Provider, Insurance Carrier, Payment Method

## Tips

- A healthy practice typically sees 50–70% of collections from insurance and 30–50% from patients.
- If patient collections are declining, cross-reference with the **Statement Activity Report** to verify statements are being sent on schedule.')

ON CONFLICT (slug) DO NOTHING;

-- =============================================================================
-- TECHNICAL / TROUBLESHOOTING (9 articles)
-- =============================================================================

INSERT INTO knowledge_articles (title, slug, category, content) VALUES

('System Running Slow — Common Fixes',
'system-running-slow-common-fixes',
'technical_troubleshooting',
'## System Running Slow — Common Fixes

If ClinicDesk is responding slowly, follow these steps in order before contacting support.

## Step 1: Check Your Internet Connection

Open a new browser tab and visit a site like google.com. ClinicDesk requires a minimum of **10 Mbps** download speed.

## Step 2: Restart the Browser

Close all open browser tabs and windows, then relaunch the browser.

## Step 3: Clear Cache and Cookies

See the article **"Clearing Cache and Cookies to Fix Display Issues"** for full instructions.

## Step 4: Reduce Open Tabs

Close any ClinicDesk tabs you are not actively using. Navigate to **Settings → Session Management** and click **End Idle Sessions**.

## Step 5: Check Workstation Resources

- On Windows: Press **Ctrl + Shift + Esc** to open Task Manager.
- On Mac: Open **Activity Monitor** from Applications → Utilities.
- ClinicDesk recommends at least **8 GB of RAM** and a modern dual-core processor.

## Step 6: Check System Status

Visit **Admin → System → Health Monitor** to view real-time server response times.

## Still Slow?

Contact ClinicDesk Support with your browser name/version, operating system, time of day, and which pages are affected.'),

('Printer Not Working with the Software',
'printer-not-working-with-the-software',
'technical_troubleshooting',
'## Printer Not Working with the Software

ClinicDesk supports printing through your browser''s native print dialog.

## Confirm Printer Setup

1. Ensure your printer is powered on and connected.
2. Print a test page from your OS to confirm the printer works.
3. Set the correct printer as the **default printer** in your OS settings.

## Printing from ClinicDesk

1. Open the record or form you wish to print.
2. Click the **Print** button or use **Ctrl + P** (Windows) / **Cmd + P** (Mac).
3. In the browser print dialog, select your printer, adjust paper size and orientation.
4. Click **Print**.

## Common Issues

**Nothing happens when I click Print:**
- Disable any pop-up blockers for your ClinicDesk domain.

**Output is cut off or misaligned:**
- In the print dialog, set margins to **None** or **Minimum**.
- Ensure **Scale** is set to **100%**.

**Label printer not printing correctly:**
- ClinicDesk label templates are formatted for **Dymo LabelWriter 450** or **Zebra ZD410** by default.
- Go to **Settings → Print Templates → Label Size** and confirm the correct label dimensions.'),

('Login Issues and Password Resets',
'login-issues-and-password-resets',
'technical_troubleshooting',
'## Login Issues and Password Resets

If you are unable to log in to ClinicDesk, follow this guide.

## Forgot Your Password

1. On the login page, click **"Forgot Password?"**.
2. Enter your email address and click **Send Reset Link**.
3. Check your inbox (and spam folder) for an email from **noreply@clinicdesk.com**.
4. Click the reset link (expires after **30 minutes**).
5. Enter a new password (minimum 8 characters, at least one number and one special character).
6. Click **Save Password** and log in.

## Account Locked

After **5 consecutive failed attempts**, your account is locked for 15 minutes. Wait and try again, or contact your Practice Administrator to unlock via **Admin → User Management → Unlock Account**.

## Common Problems

**"Invalid credentials" with correct password:**
- Ensure Caps Lock is not enabled.
- Clear your browser''s autofill data.

**Two-factor authentication (2FA) code not working:**
- Ensure your device clock is accurate — TOTP codes are time-sensitive.
- Contact your administrator to reset 2FA via **Admin → User Management → Reset 2FA**.'),

('Browser Compatibility Requirements',
'browser-compatibility-requirements',
'technical_troubleshooting',
'## Browser Compatibility Requirements

ClinicDesk is a web-based application. Using a supported and up-to-date browser is essential.

## Supported Browsers

| Browser | Minimum Version | Recommended |
|---|---|---|
| Google Chrome | 110 | Yes (preferred) |
| Microsoft Edge | 110 | Yes |
| Mozilla Firefox | 109 | Yes |
| Apple Safari | 16 | Partial support |
| Internet Explorer | Any | Not supported |

## Browser Settings Requirements

- **JavaScript**: Must be enabled
- **Cookies**: Must be allowed for your ClinicDesk domain
- **Pop-ups**: Must be allowed (required for print dialogs)
- **Local Storage**: Must not be blocked

## Mobile and Tablet

ClinicDesk is optimized for desktop use. Tablet browsers work but some features may not render on screens smaller than 10 inches. Mobile phone browsers are not officially supported.'),

('Clearing Cache and Cookies to Fix Display Issues',
'clearing-cache-and-cookies-to-fix-display-issues',
'technical_troubleshooting',
'## Clearing Cache and Cookies to Fix Display Issues

If ClinicDesk is displaying outdated information, broken layouts, or missing buttons, clearing your browser''s cache and cookies often resolves the issue.

## Google Chrome
1. Press **Ctrl + Shift + Delete** (Windows) or **Cmd + Shift + Delete** (Mac).
2. Set the time range to **All time**.
3. Check **Cookies and other site data** and **Cached images and files**.
4. Click **Clear data**.

## Microsoft Edge
1. Press **Ctrl + Shift + Delete**.
2. Set time range to **All time**.
3. Check **Cookies** and **Cached images and files**.
4. Click **Clear now**.

## Mozilla Firefox
1. Press **Ctrl + Shift + Delete** (or **Cmd + Shift + Delete**).
2. Set time range to **Everything**.
3. Check **Cookies** and **Cache**.
4. Click **OK**.

## Apple Safari
1. Click **Safari** → **Settings** → **Privacy**.
2. Click **Manage Website Data**, search for your ClinicDesk domain, and click **Remove**.
3. Then go to **Develop → Empty Caches**.

## After Clearing

Log in to ClinicDesk again. If the issue persists, try an incognito/private window. If it works there, a browser extension may be interfering.'),

('Data Backup Procedures',
'data-backup-procedures',
'technical_troubleshooting',
'## Data Backup Procedures

ClinicDesk automatically backs up your practice data on a scheduled basis.

## Automated Backup Schedule

- **Daily incremental backup:** Every night at 2:00 AM
- **Weekly full backup:** Every Sunday at 1:00 AM
- **Monthly archive:** On the 1st of each month, retained for 7 years

Retention periods: Daily (30 days), Weekly (6 months), Monthly (7 years).

## Viewing Backup History

Navigate to **Admin → System → Backup & Recovery** to see all recent backups with status, file size, and timestamp.

## Requesting a Manual Backup

1. Go to **Admin → System → Backup & Recovery**.
2. Click **Create Manual Backup**.
3. Enter a description and click **Start Backup** (typically 5–15 minutes).

## Requesting Data Restoration

Contact **ClinicDesk Support** immediately — do not make additional changes to the affected records. Provide the approximate date and time of the data loss.'),

('Connecting to the Practice Database from a New Workstation',
'connecting-to-the-practice-database-from-a-new-workstation',
'technical_troubleshooting',
'## Connecting to the Practice Database from a New Workstation

ClinicDesk is cloud-based, so there is no local database installation required.

## Step 1: Confirm Network Access

Ensure the workstation is connected to the clinic network and can reach your ClinicDesk URL via HTTPS.

## Step 2: Install a Supported Browser

Install the latest version of **Google Chrome** or **Microsoft Edge**.

## Step 3: Log In and Verify

Navigate to your ClinicDesk URL, log in, and confirm access to your usual modules.

## Step 4: Configure Peripherals (If Applicable)

**Digital X-ray / Imaging Software:**
- Download and install the ClinicDesk Bridge Connector from **Admin → Integrations → Bridge Connector → Download Installer**.

**Label Printers:**
- Install the manufacturer driver, then go to **Settings → Workstation Preferences → Default Label Printer**.

## Enterprise: Register the Workstation

Go to **Admin → Security → Trusted Devices** and click **Register This Device**.'),

('Software Update / Upgrade Instructions',
'software-update-upgrade-instructions',
'technical_troubleshooting',
'## Software Update / Upgrade Instructions

ClinicDesk is cloud-hosted, so core updates are deployed automatically. However, some companion components need manual updates.

## Automatic Application Updates

- Updates are deployed during scheduled maintenance windows (typically 2:00 AM – 4:00 AM on weekdays).
- You may be prompted to **refresh your browser** after an update.

## ClinicDesk Bridge Connector

1. Go to **Admin → Integrations → Bridge Connector**.
2. If an update is available, click **Download Update**.
3. Run the installer on each workstation. Administrator privileges required.
4. Restart the workstation.

## Verifying Your Current Version

Navigate to **Help → About ClinicDesk** to view your current application version and last update date.'),

('Error Code Reference',
'error-code-reference',
'technical_troubleshooting',
'## Error Code Reference

Common error codes displayed in ClinicDesk and how to resolve them.

### ERR-1001: Session Expired
Your login session timed out after 30 minutes of inactivity. Click **Return to Login** and sign in again.

### ERR-1002: Insufficient Permissions
Your user role does not have access to the requested feature. Contact your administrator via **Admin → User Management → Roles**.

### ERR-1003: Record Locked by Another User
Another user currently has the same record open in edit mode. Wait or ask them to close it. Admins can release locks via **Admin → System → Active Record Locks**.

### ERR-1004: Connection Timeout
The workstation lost connection to the ClinicDesk servers. Check your internet connection and reload the page.

### ERR-1005: File Upload Failed
The uploaded file exceeds the 25 MB size limit or the file type is not permitted.

### ERR-1006: Duplicate Entry Detected
A patient or record with matching identifying information already exists. Use **Patients → Search → Advanced Search** to locate duplicates.

### ERR-1007: Billing Claim Rejected
The submitted insurance claim contains missing or invalid fields. Review under **Billing → Claims → Rejected**.

### ERR-1008: Integration Sync Failed
The Bridge Connector could not communicate with the connected system. Restart the Bridge Connector service.

### ERR-1009: Report Generation Timeout
The requested report query exceeded the maximum processing time. Narrow the date range or reduce filters.

### ERR-1010: Invalid Date of Birth
The entered date of birth is in an incorrect format. Use **MM/DD/YYYY** format.

### ERR-1011: Payment Gateway Error
The integrated payment processor declined the transaction. Verify card details and retry.

### ERR-1012: Appointment Conflict
The selected time overlaps with an existing booking. Review the provider''s schedule.

### ERR-1013: Template Not Found
A referenced template no longer exists. Recreate or restore under **Settings → Templates**.

### ERR-1014: Two-Factor Authentication Required
Your account requires 2FA enrollment. Follow the prompts to set up an authenticator app.

### ERR-1015: License Seat Limit Reached
Your practice has reached the maximum concurrent users for your plan. Upgrade or deactivate unused accounts under **Admin → User Management**.')

ON CONFLICT (slug) DO NOTHING;

-- =============================================================================
-- ACCOUNT & PLANS (9 articles)
-- =============================================================================

INSERT INTO knowledge_articles (title, slug, category, content) VALUES

('ClinicDesk Plan Tiers and Pricing',
'clinicdesk-plan-tiers-and-pricing',
'account_plans',
'## ClinicDesk Plan Tiers and Pricing

ClinicDesk offers three subscription plans designed to fit practices of every size. All plans include a 14-day free trial and are billed monthly or annually (annual billing saves 20%).

## Basic — $49/month

- Up to **3 user seats**
- Up to **500 active patient records**
- Appointment scheduling & calendar management
- Basic SOAP note templates
- Patient intake forms (digital)
- Email appointment reminders
- Standard reporting dashboard
- Community support (forums + knowledge base)

## Professional — $99/month

Everything in Basic, plus:
- Up to **10 user seats**
- **Unlimited** active patient records
- Customizable clinical note templates
- Insurance eligibility verification (automated)
- Two-way SMS appointment reminders
- Treatment plan builder with e-signature
- Billing & invoicing with ERA posting
- QuickBooks integration
- Priority email & chat support
- Advanced analytics and custom reports

## Enterprise — $199/month

Everything in Professional, plus:
- **Unlimited user seats** across multiple locations
- Multi-location management dashboard
- Role-based access controls with custom permission sets
- Full REST API access
- Single Sign-On (SSO) via SAML 2.0
- Dedicated account manager
- Custom onboarding & staff training
- SLA-backed uptime guarantee (99.9%)
- Phone support + 24/7 critical incident line
- HIPAA BAA included at no extra cost

## Add-Ons

- Additional User Seats: $12/seat/month (Basic), $10/seat/month (Professional)
- SMS Booster Pack: 1,000 extra SMS credits for $8/month
- Advanced Imaging Storage: 100 GB additional storage for $15/month

To view your current plan, navigate to **Settings → Account & Billing → Subscription**.'),

('How to Upgrade Your ClinicDesk Plan',
'how-to-upgrade-your-clinicdesk-plan',
'account_plans',
'## How to Upgrade Your ClinicDesk Plan

Upgrading takes effect immediately — you will gain access to new features right away with prorated billing.

## Steps to Upgrade

1. Click your **clinic name** in the top-right corner.
2. Select **Settings** from the dropdown.
3. In the left sidebar, click **Account & Billing**, then **Subscription**.
4. Click the **Upgrade Plan** button.
5. Review the available tiers and click **Select Plan** under the desired tier.
6. Review the **Order Summary** with prorated charges.
7. Click **Confirm Upgrade**.

## After Upgrading

- New features are enabled instantly.
- Your next invoice reflects the new plan rate.
- For Enterprise plans, you''ll be directed to a **Schedule a Call** form for custom onboarding.

## Tips

- If the **Upgrade Plan** button is greyed out, your account role may not have billing permissions.'),

('How to Add Additional User Seats',
'how-to-add-additional-user-seats',
'account_plans',
'## How to Add Additional User Seats

Each ClinicDesk plan includes a set number of seats. Add more at any time without changing your base plan.

## Included Seats by Plan

| Plan | Included Seats |
|---|---|
| Basic | 3 seats |
| Professional | 10 seats |
| Enterprise | Unlimited |

## How to Add Seats

1. Go to **Settings → Account & Billing → Subscription**.
2. Under **User Seats**, click **Add Seats**.
3. Select the number of additional seats needed.
4. Review the prorated charge and click **Add Seats**.

## Seat Pricing

- Basic plan: $12 per additional seat/month
- Professional plan: $10 per additional seat/month
- Enterprise plan: Unlimited — no additional charge

## Inviting Users

After adding seats, go to **Settings → Team & Permissions → Users** and click **Invite User**.

## Removing Seats

Navigate to **Settings → Account & Billing → Subscription**, click **Manage Seats**, and decrease the number. Reductions take effect at the next billing cycle.'),

('How to View Your Current Subscription and Billing',
'how-to-view-your-current-subscription-and-billing',
'account_plans',
'## How to View Your Current Subscription and Billing

Only Account Owners and Billing Admins can access billing details.

## Accessing the Billing Dashboard

Click your **clinic name** → **Settings** → **Account & Billing**.

## Subscription Tab

Shows current plan, billing cycle, renewal date, seat count, active add-ons, and next invoice amount.

## Invoices Tab

Displays a complete history of all charges with invoice date, amount, payment status, and PDF download links.

## Payment Methods Tab

View, add, or remove credit/debit cards and ACH bank accounts. ClinicDesk accepts Visa, Mastercard, American Express, and ACH.

## Failed Payments

ClinicDesk retries after 3 days and 7 days. If unresolved within 14 days, the account is suspended. Update your payment method and click **Retry Payment**.'),

('Feature Comparison Between ClinicDesk Plan Tiers',
'feature-comparison-between-clinicdesk-plan-tiers',
'account_plans',
'## Feature Comparison Between ClinicDesk Plan Tiers

| Feature | Basic ($49/mo) | Professional ($99/mo) | Enterprise ($199/mo) |
|---|---|---|---|
| User Seats | 3 (+ $12/seat) | 10 (+ $10/seat) | Unlimited |
| Active Patient Records | 500 | Unlimited | Unlimited |
| Appointment Scheduling | Yes | Yes | Yes |
| Digital Intake Forms | Yes | Yes | Yes |
| Custom Note Templates | No | Yes | Yes |
| Two-Way SMS Reminders | No | Yes | Yes |
| Insurance Eligibility Verification | No | Yes | Yes |
| Treatment Plan Builder | No | Yes | Yes |
| Billing with ERA Posting | Basic | Full | Full |
| QuickBooks Integration | No | Yes | Yes |
| Custom Reports | No | Yes | Yes |
| Multi-Location Management | No | No | Yes |
| REST API Access | No | No | Yes |
| SSO / SAML 2.0 | No | No | Yes |
| HIPAA BAA | $25/mo add-on | Included | Included |
| Support | Community | Email & Chat | Phone + Dedicated Manager |
| SLA Uptime Guarantee | No | No | 99.9% |

To upgrade, go to **Settings → Account & Billing → Subscription** and click **Upgrade Plan**.'),

('How to Request a Feature or Submit Feedback',
'how-to-request-a-feature-or-submit-feedback',
'account_plans',
'## How to Request a Feature or Submit Feedback

Your feedback directly influences our product roadmap.

## Submitting a Feature Request

1. Click the **Help** icon (question mark) in the bottom-left corner.
2. Select **Share Feedback** from the menu.
3. Click the **Feature Request** tab.
4. Enter a title and description of your idea.
5. Optionally attach a screenshot.
6. Click **Submit Request**.

## Voting on Existing Requests

Navigate to **Help → Product Roadmap** (or visit **roadmap.clinicdesk.com**) to browse and upvote community requests.

## Enterprise Feedback

Enterprise customers have a dedicated channel through their Account Manager.'),

('Cancellation Policy and How to Cancel Your Subscription',
'cancellation-policy-and-how-to-cancel-your-subscription',
'account_plans',
'## Cancellation Policy and How to Cancel Your Subscription

## Cancellation Policy

- **Monthly plans**: Cancel anytime. Account remains active until the end of the billing period.
- **Annual plans**: Cancel anytime, but no refunds for unused months. Account remains active through the paid term.
- **Free trial**: Cancel anytime during the 14-day trial with no charge.

There are no cancellation fees.

## How to Request Cancellation

Cancellation must be completed by contacting our support team directly:

1. Navigate to **Help → Contact Support**.
2. Select **Billing & Account** as the topic.
3. In the subject line, write: *"Cancellation Request – [Your Clinic Name]"*
4. Click **Submit**.

A billing team member will respond within **1 business day**. You can also email **billing@clinicdesk.com** or call **1-888-254-7732**.

## Before You Cancel

- **Export your patient data** (see the Data Export article)
- **Download all invoices** from **Settings → Account & Billing → Invoices**
- **Notify your team**

## After Cancellation

Patient data is retained in read-only archive for **90 days**, then permanently deleted. You may request a final export during this window.'),

('Data Export When Changing or Cancelling Your Plan',
'data-export-when-changing-or-cancelling-your-plan',
'account_plans',
'## Data Export When Changing or Cancelling Your Plan

You own your data, and ClinicDesk makes it accessible for export at any time.

## What Can Be Exported

- Patient Records (demographics, contacts, insurance)
- Clinical Notes (SOAP notes, treatment records, attachments)
- Appointment History
- Invoices & Payments (CSV)
- Treatment Plans (PDF per patient)
- Intake Forms (CSV)

## How to Export

1. Navigate to **Settings → Data & Privacy → Export Data**.
2. Select data categories and date range.
3. Choose format: **CSV** (tabular) or **JSON** (structured, recommended for migrations).
4. Click **Request Export**.
5. You''ll receive an email with a **secure download link** (expires in 72 hours).

## Export by Plan

| Plan | Self-Service Export | API Export |
|---|---|---|
| Basic | CSV only | No |
| Professional | CSV + JSON | No |
| Enterprise | CSV + JSON | Yes (REST API) |

## Tips

- Export before your billing period ends if cancelling — self-service export is removed when the account closes.
- Enterprise customers can request a **Managed Migration** service through their Account Manager.'),

('API Access: Which Plans Include It and How to Get Started',
'api-access-which-plans-include-it-and-how-to-get-started',
'account_plans',
'## API Access: Which Plans Include It and How to Get Started

The ClinicDesk REST API allows your technical team to integrate ClinicDesk with external systems and automate workflows.

## API Access by Plan

| Plan | API Access |
|---|---|
| Basic | Not included |
| Professional | Not included |
| Enterprise | Included |

## What the API Supports

- **Patients**: Create, read, update, and search
- **Appointments**: List, create, update, cancel
- **Clinical Notes**: Read and create SOAP notes
- **Invoices**: Retrieve billing records and payment status
- **Users**: List users and their roles
- **Webhooks**: Subscribe to real-time events

All endpoints use **JSON** over **HTTPS**. Base URL: `https://api.clinicdesk.com/v2/`

## Generating an API Key

1. Navigate to **Settings → Integrations → API Keys**.
2. Click **Generate New API Key**.
3. Enter a label and select permission scopes.
4. Click **Generate**. Copy the key immediately — it will not be displayed again.

## Rate Limits

- 600 requests per minute per API key
- 50,000 requests per day per account

## Documentation

Full API reference at **developers.clinicdesk.com**.')

ON CONFLICT (slug) DO NOTHING;
