import os
import pickle
import streamlit as st
import matplotlib.pyplot as plt


# Load courses and similarity data
courses_list = pickle.load(open('courses.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Function to recommend courses
def recommend(course):
    index = courses_list[courses_list['course_name'] == course].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_course_names = []
    for i in distances[1:7]:
        course_name = courses_list.iloc[i[0]].course_name
        recommended_course_names.append(course_name)

    return recommended_course_names

# Function to generate a quiz for a given subject
def generate_quiz(subject):
    # Define quiz questions for various subjects
    quiz_data = {
        'Finance for Managers': [
            {
                "question": "What is the formula for calculating ROI (Return on Investment)?",
                "options": ["Profit / Initial Investment", "Revenue / Expenses", "Profit / Revenue"],
                "correct_option": 0
            },
            {
                "question": "What does GDP stand for?",
                "options": ["Global Domestic Product", "Gross Domestic Product", "General Domestic Price"],
                "correct_option": 1
            },
            {
                "question": "What is a balance sheet used to show?",
                "options": ["Income and Expenses", "Assets and Liabilities", "Customer Orders"],
                "correct_option": 1
            },
            {
                "question": "What is the time value of money (TVM) concept in finance?",
                "options": ["Money earned today is worth less than money earned in the future", "Money earned today is worth more than money earned in the future", "Money earned today has no value"],
                "correct_option": 0
            },
            {
                "question": "What is diversification in investment?",
                "options": ["Putting all your money into one investment", "Spreading your investments across different assets", "Holding cash in a savings account"],
                "correct_option": 1
            },
            {
                "question": "What is a dividend in finance?",
                "options": ["A type of loan", "A distribution of a company's earnings to its shareholders", "An insurance policy"],
                "correct_option": 1
            },
            {
                "question": "What is the primary goal of financial management in a business?",
                "options": ["Maximize profits", "Minimize losses", "Maximize shareholder wealth"],
                "correct_option": 2
            },
            {
                "question": "What is the role of a financial manager?",
                "options": ["Provide legal advice to the company", "Make financial decisions for the company", "Manage the company's marketing activities"],
                "correct_option": 1
            },
            {
                "question": "What is the stock market?",
                "options": ["A physical marketplace where goods are traded", "A virtual marketplace where stocks and securities are bought and sold", "A bank's customer service desk"],
                "correct_option": 1
            },
            {
                "question": "What is inflation in finance?",
                "options": ["A decrease in the prices of goods and services", "A situation where the economy does not grow", "An increase in the prices of goods and services over time"],
                "correct_option": 2
            },
        ],
        'History': [
            {
                "question": "Who was the first President of the United States?",
                "options": ["George Washington", "Thomas Jefferson", "Abraham Lincoln"],
                "correct_option": 0
            },
            {
                "question": "What ancient civilization is known for the construction of the Great Wall?",
                "options": ["Roman Empire", "Greek Empire", "Chinese Empire"],
                "correct_option": 2
            },
            {
                "question": "What event is often considered the start of World War I?",
                "options": ["The sinking of the Titanic", "The assassination of Archduke Franz Ferdinand", "The signing of the Treaty of Versailles"],
                "correct_option": 1
            },
            {
                "question": "Who wrote the 'Declaration of Independence' of the United States?",
                "options": ["Benjamin Franklin", "George Washington", "Thomas Jefferson"],
                "correct_option": 2
            },
            {
                "question": "In which year did the United States declare its independence?",
                "options": ["1776", "1789", "1801"],
                "correct_option": 0
            },
            {
                "question": "Who was the leader of the Soviet Union during the Cuban Missile Crisis?",
                "options": ["Vladimir Putin", "Mikhail Gorbachev", "Nikita Khrushchev"],
                "correct_option": 2
            },
            {
                "question": "Which ancient civilization is famous for inventing the wheel?",
                "options": ["Egyptian civilization", "Sumerian civilization", "Mayan civilization"],
                "correct_option": 1
            },
            {
                "question": "Who is known for his theory of relativity?",
                "options": ["Isaac Newton", "Albert Einstein", "Galileo Galilei"],
                "correct_option": 1
            },
            {
                "question": "What is the Magna Carta?",
                "options": ["A famous painting", "A medieval legal document", "A musical composition by Beethoven"],
                "correct_option": 1
            },
            {
                "question": "What was the main cause of the French Revolution?",
                "options": ["High taxes", "Monarchy", "Social inequality"],
                "correct_option": 2
            },
        ],
        # Add more subjects and their respective questions as needed
    }

    return quiz_data.get(subject, [])

# Streamlit app
st.markdown("<h2 style='text-align: center; color: blue;'>COURSE RECOMMENDATION SYSTEM</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: black;'>Find courses according to your grasping power!</h4>", unsafe_allow_html=True)

st.sidebar.header("User Settings")
selected_course = st.sidebar.selectbox("Select a course you like:", courses_list['course_name'].values)
selected_subject = st.sidebar.selectbox("Select the subject of the quiz:", ['Finance for Managers', 'History'])

if st.sidebar.button('Show Recommended Courses'):
    st.write("Recommended Courses based on your interests are:")
    recommended_course_names = recommend(selected_course)
    st.write(recommended_course_names)

st.sidebar.markdown("<h6 style='text-align: center; color: red;'>Find the right course for you!</h6>", unsafe_allow_html=True)


if selected_subject:
    st.header(f"Quiz for {selected_subject}")
    quiz_questions = generate_quiz(selected_subject)
    if not quiz_questions:
        st.write("No quiz available for this subject.")
    else:
        score = 0
        selected_options = []

        for i, question in enumerate(quiz_questions, start=1):
            st.subheader(f"Question {i}: {question['question']}")
            options = question['options']

            # Create a unique radio group for each question
            selected_option = st.radio(f"Options for Question {i}", options)
            selected_options.append(selected_option)

        if st.button('Submit Quiz'):
            for i, question in enumerate(quiz_questions, start=1):
                if selected_options[i-1] == question['options'][question['correct_option']]:
                    score += 1

            st.write(f"You scored {score} out of {len(quiz_questions)}.")

            # Create a bar chart to visualize the user's score
            fig, ax = plt.subplots()
            ax.bar(['Correct', 'Incorrect'], [score, len(quiz_questions) - score])
            ax.set_xlabel('Quiz Results')
            ax.set_ylabel('Number of Questions')
            ax.set_title('Quiz Score')
            st.pyplot(fig)

            # Adjust the recommendations based on the score
            recommended_course_names = recommend(selected_course)
            if score < 4 :
                st.write("You might want to explore some introductory courses.")
                st.write("Recommended courses for you:")
                for course in recommended_course_names[:3]:
                    st.write(course)
            elif score < 7:
                st.write("You have a decent understanding. Consider exploring more advanced courses.")
                st.write("Recommended courses for you:")
                for course in recommended_course_names[3:6]:
                    st.write(course)
            else:
                st.write("You have a strong grasp of this subject. Look into advanced courses and specializations.")
                st.write("Recommended advanced courses for you:")
                for course in recommended_course_names[6:9]:
                    st.write(course)







