# Zain Hackathon Entry
## Payment Agentic System
This project is an entry to Zain's hackathon, as of now, this is a prototype to be submitted at 2026-9-28.  

## How To Run It

You need python installed, then:

```

pip install uv # install the package manager
uv sync # Install the dependencies
uv run fastapi dev # Run the app

```

## How It Works

This is the trajectory we are aiming for when we get our hands on an agnet (currently most of them are paid or have not working free versions).  

---    

Know that the agent below was a fresh one only provided with the `system_prompt.md` file you can find in `src/zain_hackathon_entry`:  


```

You said:
تكدر تشوفلي منو اني حافظه بالجهات


ChatGPT Executed:

curl -X GET "https://YOUR_API_HOST/api/acquaintances" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

{"detail":"Acquaintances not found. Please add any."}


ChatGPT said:
ما عندك حالياً أي جهات محفوظة بالتطبيق.

إذا تريد تحول فلوس لشخص، گلي اسمه أو اليوزرنيم والمبلغ، وأنا أكمّل وياك خطوة بخطوة.


You said:
اليوزر مالته ahmed احفظه كاحمد ابو خشم وانوب دزله 20 الف


ChatGPT Executed:

curl -X GET "https://YOUR_API_HOST/api/users/username/ahmed" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

{"username":"ahmed","id":2}


curl -X POST "https://YOUR_API_HOST/api/acquaintances" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "acquaintance_name":"أحمد أبو خشم",
    "notes_on_acquaintance":"",
    "username":"ahmed"
  }'

{"acquaintance_name":"أحمد أبو خشم","notes_on_acquaintance":"","id":1}


curl -X POST "https://YOUR_API_HOST/api/transfer/make_request" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount":20000,"receiver_id":2}'

{"message":"CONFIRMATION_NEEDED","request":{"amount":20000,"receiver_id":2,"id":1,"sender_id":1,"date":"2026-09-25T13:52:39.280459Z"}}


ChatGPT said:
طلب التحويل رقم 1 إلى أحمد أبو خشم جاهز، وقيمته 20,000 ألف دينار.

تأكّدلي: أكمّل وأأكد التحويل؟


You said:
أي دزله


ChatGPT said:
تمام، راح نأكد طلب التحويل رقم 1 إلى أحمد أبو خشم بمبلغ 20,000 ألف دينار.


ChatGPT Executed:
curl -X POST "https://YOUR_API_HOST/api/transfer/confirm_request/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

{"message":"Transaction confirmed.","request":{"amount":20000,"receiver_id":2,"id":1,"sender_id":1,"date":"2026-09-25T13:52:39.280459"}}


ChatGPT said:
تم التحويل بنجاح ✅

المبلغ: 20,000 ألف دينار

المستلم: أحمد أبو خشم

رقم العملية: 1

الحالة: تم التأكيد


You said:
نويص, اشكرك


ChatGPT said:
العفو حبيبي، بالخدمة دوم 🌹 الله يوفقك.

```