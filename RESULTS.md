# Test Results — NL2SQL System

## Summary

Total Questions: 20  
Correct: 16  
Partial: 3  
Failed: 1  

---

## Results

### 1. How many patients do we have?
SQL:
SELECT COUNT(*) FROM patients  
Status: ✅ Correct  

---

### 2. List all doctors and their specializations
SQL:
SELECT name, specialization FROM doctors  
Status: ✅ Correct  

---

### 3. Show me appointments for last month
SQL:
SELECT * FROM appointments WHERE appointment_date >= datetime('now','-1 month')  
Status: ✅ Correct  

---

### 4. Which doctor has the most appointments?
SQL:
SELECT doctor_id, COUNT(*) FROM appointments GROUP BY doctor_id ORDER BY COUNT(*) DESC LIMIT 1  
Status: ✅ Correct  

---

### 5. What is the total revenue?
SQL:
SELECT SUM(total_amount) FROM invoices  
Status: ✅ Correct  

---

### 6. Show revenue by doctor
Status: ⚠️ Partial (join complexity issue)

---

### 7. Cancelled appointments last quarter
Status: ✅ Correct  

---

### 8. Top 5 patients by spending
Status: ✅ Correct  

---

### 9. Average treatment cost by specialization
Status: ⚠️ Partial  

---

### 10. Monthly appointment count
Status: ✅ Correct  

---

### 11. City with most patients
Status: ✅ Correct  

---

### 12. Patients with >3 visits
Status: ⚠️ Partial  

---

### 13. Unpaid invoices
Status: ✅ Correct  

---

### 14. No-show percentage
Status: ❌ Failed (complex aggregation)

---

### 15. Busiest day
Status: ✅ Correct  

---

### 16. Revenue trend
Status: ✅ Correct  

---

### 17. Avg duration by doctor
Status: ✅ Correct  

---

### 18. Overdue invoices patients
Status: ✅ Correct  

---

### 19. Revenue by department
Status: ✅ Correct  

---

### 20. Patient registration trend
Status: ✅ Correct  

---

## Observations

- Simple queries perform very well
- JOIN-heavy queries sometimes partially incorrect
- Memory improves accuracy
- Aggregation edge cases need tuning

---

## Conclusion

The system successfully handles most real-world queries and demonstrates strong NL2SQL capability using Vanna 2.0 with Groq LLM.