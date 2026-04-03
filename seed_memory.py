import asyncio
import uuid

from vanna_setup import agent
from vanna.core.tool import ToolContext
from vanna.core.user import User

SEED_EXAMPLES = [
    {
        "question": "How many patients do we have?",
        "sql": "SELECT COUNT(*) AS total_patients FROM patients;"
    },
    {
        "question": "List all doctors and their specializations",
        "sql": "SELECT name, specialization FROM doctors ORDER BY name;"
    },
    {
        "question": "Which city has the most patients?",
        "sql": """
            SELECT city, COUNT(*) AS patient_count
            FROM patients
            GROUP BY city
            ORDER BY patient_count DESC
            LIMIT 1;
        """
    },
    {
        "question": "Show all female patients from Hyderabad",
        "sql": """
            SELECT id, first_name, last_name, city, gender
            FROM patients
            WHERE gender = 'F' AND city = 'Hyderabad'
            ORDER BY last_name, first_name;
        """
    },
    {
        "question": "Show appointments count by doctor",
        "sql": """
            SELECT d.name, COUNT(a.id) AS appointment_count
            FROM doctors d
            LEFT JOIN appointments a ON d.id = a.doctor_id
            GROUP BY d.id, d.name
            ORDER BY appointment_count DESC;
        """
    },
    {
        "question": "Which doctor has the most appointments?",
        "sql": """
            SELECT d.name, COUNT(a.id) AS appointment_count
            FROM doctors d
            JOIN appointments a ON d.id = a.doctor_id
            GROUP BY d.id, d.name
            ORDER BY appointment_count DESC
            LIMIT 1;
        """
    },
    {
        "question": "Show completed appointments",
        "sql": """
            SELECT id, patient_id, doctor_id, appointment_date, status
            FROM appointments
            WHERE status = 'Completed'
            ORDER BY appointment_date DESC;
        """
    },
    {
        "question": "Show appointments for the last 3 months",
        "sql": """
            SELECT id, patient_id, doctor_id, appointment_date, status
            FROM appointments
            WHERE appointment_date >= datetime('now', '-3 months')
            ORDER BY appointment_date DESC;
        """
    },
    {
        "question": "Show monthly appointment count for the past 6 months",
        "sql": """
            SELECT strftime('%Y-%m', appointment_date) AS month,
                   COUNT(*) AS appointment_count
            FROM appointments
            WHERE appointment_date >= datetime('now', '-6 months')
            GROUP BY strftime('%Y-%m', appointment_date)
            ORDER BY month;
        """
    },
    {
        "question": "How many cancelled appointments last quarter?",
        "sql": """
            SELECT COUNT(*) AS cancelled_count
            FROM appointments
            WHERE status = 'Cancelled'
              AND appointment_date >= datetime('now', '-3 months');
        """
    },
    {
        "question": "What is the total revenue?",
        "sql": """
            SELECT SUM(total_amount) AS total_revenue
            FROM invoices;
        """
    },
    {
        "question": "Show unpaid invoices",
        "sql": """
            SELECT id, patient_id, invoice_date, total_amount, paid_amount, status
            FROM invoices
            WHERE status IN ('Pending', 'Overdue')
            ORDER BY invoice_date DESC;
        """
    },
    {
        "question": "What is the average treatment cost?",
        "sql": """
            SELECT AVG(cost) AS average_treatment_cost
            FROM treatments;
        """
    },
    {
        "question": "Show revenue trend by month",
        "sql": """
            SELECT strftime('%Y-%m', invoice_date) AS month,
                   SUM(total_amount) AS monthly_revenue
            FROM invoices
            GROUP BY strftime('%Y-%m', invoice_date)
            ORDER BY month;
        """
    },
    {
        "question": "Top 5 patients by spending",
        "sql": """
            SELECT p.id,
                   p.first_name,
                   p.last_name,
                   SUM(i.total_amount) AS total_spending
            FROM patients p
            JOIN invoices i ON p.id = i.patient_id
            GROUP BY p.id, p.first_name, p.last_name
            ORDER BY total_spending DESC
            LIMIT 5;
        """
    },
]


async def seed_memory():
    saved = 0

    user = User(
        id="default_user",
        email="default_user@example.com",
        group_memberships=["admin", "user"],
    )

    context = ToolContext(
        user=user,
        conversation_id="seed-conversation",
        request_id=str(uuid.uuid4()),
        agent_memory=agent.agent_memory,
    )

    for item in SEED_EXAMPLES:
        try:
            await agent.agent_memory.save_tool_usage(
                question=item["question"],
                tool_name="run_sql",
                args={"sql": item["sql"].strip()},
                context=context,
                success=True,
            )
            saved += 1
            print(f"Saved: {item['question']}")
        except Exception as e:
            print(f"Failed to save '{item['question']}': {e}")

    print(f"\nSeeded {saved} question-SQL pairs into agent memory.")


if __name__ == "__main__":
    asyncio.run(seed_memory())