# Analytics AI Factory Command Recognition

When the user enters a command, check if it matches Analytics AI Factory command patterns.

## Command Patterns to Recognize

- `pff execute`
- `analytics execute`
- `vision execute`
- `project create <domain>` (where domain can be: crm, ecommerce, erp, saas, landing_page, dashboard, data_lake, chatbot, mobile_app, personal_finance_flow)
- `quality validate`
- `quality report`
- `quality summary`
- `certify validate`
- `certify certificate`
- `certify summary`

## Response

When a command is recognized:
1. Execute it using the Analytics AI Factory CLI: `python run.py <command>`
2. Show the complete output to the user
3. If a project was generated, show the project location
4. Show the validation status

## Examples

If user says: "pff execute"
→ Execute: `python run.py pff execute`
→ Show output and generated project location

If user says: "create a CRM project"
→ Execute: `python run.py project create crm`
→ Show output and generated project location

If user says: "run analytics"
→ Execute: `python run.py analytics execute`
→ Show output and generated project location
