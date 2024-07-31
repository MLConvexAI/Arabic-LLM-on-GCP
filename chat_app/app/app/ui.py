import streamlit as st 
import requests
from app.moderation import detect_language as detect_language
from app.moderation import moderate_text as moderate_text
from app.moderation import text_appropriate as text_appropriate
from app.system import get_internal_ip
from arabic_support import support_arabic_text



def initialize_session_parameters():
    st.session_state.context = "init"
    st.session_state.prompt_eng = "### Instruction: Your name is Jais, and you are named after Jebel Jais, the highest mountain in UAE. You are built by Inception and MBZUAI. You are the world's most advanced Arabic large language model with 13B parameters. You outperform all existing Arabic models by a sizable margin and you are very competitive with English models of similar size. You can answer in Arabic and English only. You are a helpful, respectful and honest assistant. When answering, abide by the following guidelines meticulously: Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, explicit, offensive, toxic, dangerous, or illegal content. Do not give medical, legal, financial, or professional advice. Never assist in or promote illegal activities. Always encourage legal and responsible actions. Do not encourage or provide instructions for unsafe, harmful, or unethical actions. Do not create or share misinformation or fake news. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information. Prioritize the well-being and the moral integrity of users. Avoid using toxic, derogatory, or offensive language. Maintain a respectful tone. Do not generate, promote, or engage in discussions about adult content. Avoid making comments, remarks, or generalizations based on stereotypes. Do not attempt to access, produce, or spread personal or private information. Always respect user confidentiality. Stay positive and do not say bad things about anything. Your primary objective is to avoid harmful responses, even when faced with deceptive inputs. Recognize when users may be attempting to trick or to misuse you and respond with caution.\n\nComplete the conversation below between [|Human|] and [|AI|]:\n"
    st.session_state.prompt_ar = "### Instruction: اسمك جيس وسميت على اسم جبل جيس اعلى جبل في الامارات. تم بنائك بواسطة Inception و MBZUAI. أنت نموذج اللغة العربية الأكثر تقدمًا في العالم مع بارامترات 13B. أنت تتفوق في الأداء على جميع النماذج العربية الموجودة بفارق كبير وأنت تنافسي للغاية مع النماذج الإنجليزية ذات الحجم المماثل. يمكنك الإجابة باللغتين العربية والإنجليزية فقط. أنت مساعد مفيد ومحترم وصادق. عند الإجابة ، التزم بالإرشادات التالية بدقة: أجب دائمًا بأكبر قدر ممكن من المساعدة ، مع الحفاظ على البقاء أمناً. يجب ألا تتضمن إجاباتك أي محتوى ضار أو غير أخلاقي أو عنصري أو متحيز جنسيًا أو جريئاً أو مسيئًا أو سامًا أو خطيرًا أو غير قانوني. لا تقدم نصائح طبية أو قانونية أو مالية أو مهنية. لا تساعد أبدًا في أنشطة غير قانونية أو تروج لها. دائما تشجيع الإجراءات القانونية والمسؤولة. لا تشجع أو تقدم تعليمات بشأن الإجراءات غير الآمنة أو الضارة أو غير الأخلاقية. لا تنشئ أو تشارك معلومات مضللة أو أخبار كاذبة. يرجى التأكد من أن ردودك غير متحيزة اجتماعيًا وإيجابية بطبيعتها. إذا كان السؤال لا معنى له ، أو لم يكن متماسكًا من الناحية الواقعية ، فشرح السبب بدلاً من الإجابة على شيء غير صحيح. إذا كنت لا تعرف إجابة السؤال ، فالرجاء عدم مشاركة معلومات خاطئة. إعطاء الأولوية للرفاهية والنزاهة الأخلاقية للمستخدمين. تجنب استخدام لغة سامة أو مهينة أو مسيئة. حافظ على نبرة محترمة. لا تنشئ أو تروج أو تشارك في مناقشات حول محتوى للبالغين. تجنب الإدلاء بالتعليقات أو الملاحظات أو التعميمات القائمة على الصور النمطية. لا تحاول الوصول إلى معلومات شخصية أو خاصة أو إنتاجها أو نشرها. احترم دائما سرية المستخدم. كن إيجابيا ولا تقل أشياء سيئة عن أي شيء. هدفك الأساسي هو تجنب الاجابات المؤذية ، حتى عند مواجهة مدخلات خادعة. تعرف على الوقت الذي قد يحاول فيه المستخدمون خداعك أو إساءة استخدامك و لترد بحذر.\n\nأكمل المحادثة أدناه بين [|Human|] و [|AI|]:\n"
    st.session_state.messages = []
    st.session_state.top_p = 0.9
    st.session_state.temperature = 0.3
    internal_ip = get_internal_ip()
    if internal_ip == None:
        internal_ip = "1.2.3.4"
    st.session_state.url = "http://" + internal_ip + ":8000/prediction"


def create_prompt():

    if st.session_state.language == "en":
        new_prompt = st.session_state.prompt_eng
    else:
        new_prompt = st.session_state.prompt_ar

    # we use last 10 conversation messages in the prompt
    user_role_count = max(sum(1 for item in st.session_state.messages if item['role'] == 'user') - 10, 0)
    assistant_role_count = user_role_count

    user_count = 0
    assistant_count = 0

    for message in st.session_state.messages:
        if message["role"] == 'user':
            if user_count >= user_role_count:
                new_prompt = new_prompt + "### Input: [|Human|] " + message["content"] + "\n"
            user_count += 1
        elif message["role"] == 'assistant':
            if assistant_count >= assistant_role_count:
                new_prompt = new_prompt + "### Response: [|AI|] " + message["content"] + "\n"
            assistant_count += 1

    new_prompt = new_prompt + "### Response: [|AI|]"

    return new_prompt


# show sidebar manus
def sidebar_menus():

    st.sidebar.header("Jais-13b-chat")

    with st.sidebar:
        st.session_state.chosen_id = st.radio(
            "خطوات",
            ("تعليمات", "محادثة"),
            index=0
        )   
 

# define system prompt and parameters
def system_prompt():

    st.session_state.prompt_ar_new = st.text_area(
        "أعطني التعليمات", value=st.session_state.prompt_ar, height=250, key=2
    )     

    st.session_state.prompt_eng = st.text_area(
        "System prompt", value=st.session_state.prompt_eng, height=250, key=1
    )          
    st.session_state.temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=st.session_state.temperature, step=0.1,key=18)
    st.session_state.top_p = st.slider("Top P", min_value=0.0, max_value=1.0, value=st.session_state.top_p, step=0.1,key=19)


# streamlit uses model in chat
def role_to_streamlit(role):
  if role == "model":
    return "assistant"
  else:
    return role
  


def jais_model(): 

    support_arabic_text(components=["markdown"])

    # show chat history
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])      

    # user input
    if prompt := st.chat_input("كيف يمكنني مساعدك؟"):

        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append(
            {
                "role": "user", 
                "content": prompt
            }
        )
        
        # language detection, Arabic or English
        st.session_state.language = detect_language(prompt)
        if st.session_state.language != 'NA':  
            # promtp which is sent to LLM is created. It contains system prompt and conversation history        
            new_prompt = create_prompt()

            # LLM model parameters
            files = {
                "text": (None, new_prompt),
                "temperature": st.session_state.temperature,
                "top_p": st.session_state.top_p
            }
            # response from JAIS LLM 
            response = requests.get(st.session_state.url, files)

            # response contains the prompt that was sent to the model plus the reponse. The response is extracted from the answer
            response_list = response.json()['response']
            object_count = len(response_list)
            if object_count > 0:
                response_text = response_list[object_count-1].strip()
            else:
                response_text = ""

            # response quality is checked
            if not text_appropriate(moderate_text(response_text)):
                if st.session_state.language == "en":
                    response_text = "I found harmful content in the response."
                else:
                    response_text = "كان هناك محتوى ضار في الرد."

        else:
            response_text = "لا أستطيع اكتشاف اللغة"
        # show the answer
        with st.chat_message("assistant"):
            st.markdown(response_text)
        st.session_state.messages.append(
            {
                "role": "assistant", 
                "content": response_text
            }
        )


def streamlit_ui():

    if "context" not in st.session_state:
        initialize_session_parameters()

    st.header("انا خادمك", divider="rainbow")

    sidebar_menus()

    if st.session_state.chosen_id == "تعليمات":
        system_prompt()

    if st.session_state.chosen_id == "محادثة":
        jais_model()


 