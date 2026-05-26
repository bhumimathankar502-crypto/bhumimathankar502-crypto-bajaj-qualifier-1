import requests
import time

# ── DETAILS ──────────────────────────────────────────────
NAME   = "Bhumi Mathankar"
REG_NO = "0827AL231043"
EMAIL  = "bhumimathankar230498@acropolis.in"

# ── SQL QUERY (Even reg → Question 2) ────────────────────
SQL_QUERY = """SELECT e1.EMP_ID, e1.FIRST_NAME, e1.LAST_NAME, d.DEPARTMENT_NAME, COUNT(e2.EMP_ID) AS YOUNGER_EMPLOYEES_COUNT FROM EMPLOYEE e1 JOIN DEPARTMENT d ON e1.DEPARTMENT = d.DEPARTMENT_ID LEFT JOIN EMPLOYEE e2 ON e1.DEPARTMENT = e2.DEPARTMENT AND e2.DOB > e1.DOB GROUP BY e1.EMP_ID, e1.FIRST_NAME, e1.LAST_NAME, d.DEPARTMENT_NAME ORDER BY e1.EMP_ID DESC"""

# ── STEP 1: Generate Webhook ──────────────────────────────
def generate_webhook():
    print("\n========================================")
    print("  STEP 1: Generating Webhook")
    print("========================================")
    url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
    payload = {"name": NAME, "regNo": REG_NO, "email": EMAIL}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code : {response.status_code}")
    print(f"Response    : {response.text}")

    data = response.json()
    webhook     = data.get("webhook") or data.get("webhookUrl")
    access_token = data.get("accessToken") or data.get("access_token") or data.get("token")

    if not webhook or not access_token:
        raise Exception(f"Missing webhook/token in response: {data}")

    print(f"\nWebhook URL  : {webhook}")
    print(f"Access Token : {access_token}")
    return webhook, access_token

# ── STEP 2: SQL Query ─────────────────────────────────────
def get_sql_query():
    print("\n========================================")
    print("  STEP 2: SQL Query (Even → Question 2)")
    print("========================================")
    print(SQL_QUERY)
    return SQL_QUERY

# ── STEP 3: Submit Answer ─────────────────────────────────
def submit_answer(webhook, access_token, sql_query):
    print("\n========================================")
    print("  STEP 3: Submitting Answer")
    print("========================================")
    headers = {
        "Authorization": access_token,
        "Content-Type": "application/json"
    }
    payload = {"finalQuery": sql_query}

    for attempt in range(1, 5):
        print(f"\nAttempt {attempt}...")
        response = requests.post(webhook, json=payload, headers=headers)
        print(f"Status Code : {response.status_code}")
        print(f"Response    : {response.text}")

        if response.status_code in (200, 201):
            print("\n✅ Answer submitted successfully!")
            return
        else:
            print(f"❌ Failed. Retrying in 2 seconds...")
            time.sleep(2)

    print("\n❌ All 4 attempts failed. Check token or query.")

# ── MAIN ──────────────────────────────────────────────────
if __name__ == "__main__":
    print("========================================")
    print("  Bajaj Finserv Health | Qualifier 1")
    print("  Name  : Bhumi Mathankar")
    print("  RegNo : 0827AL231043")
    print("========================================")

    webhook, access_token = generate_webhook()
    sql_query = get_sql_query()
    submit_answer(webhook, access_token, sql_query)
