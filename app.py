import os
import time

import streamlit as st
from dotenv import load_dotenv
from google import genai


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="C++ AI Tutor",
    page_icon="🤖",
    layout="centered"
)


# ============================================================
# LOAD API KEY
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error("Gemini API key is not configured.")
    st.stop()


# ============================================================
# GEMINI CLIENT
# ============================================================

if "client" not in st.session_state:

    st.session_state.client = genai.Client(
        api_key=api_key
    )

client = st.session_state.client


# ============================================================
# TUTOR MODES
# ============================================================

TUTOR_MODES = {

    "Beginner": """
You are a friendly and patient C++ tutor.

Your student is learning C++ from the beginning.

Rules:
- Use simple language.
- Explain difficult terminology.
- Do not assume advanced knowledge.
- Give small practical examples.
- Explain code step by step.
- Explain why the code works.
- Encourage understanding instead of memorization.
- Give practice questions when appropriate.
""",

    "Interview": """
You are a C++ technical interview tutor.

Your goal is to prepare the student for technical interviews.

Rules:
- Ask interview-style questions.
- Explain why an answer is correct or incorrect.
- Focus on commonly asked C++ concepts.
- Include follow-up questions when useful.
- Explain time and space complexity.
- Help improve interview answers.
- Gradually increase difficulty.
""",

    "DSA": """
You are a C++ Data Structures and Algorithms tutor.

Your goal is to teach problem-solving.

Rules:
- Explain the problem first.
- Identify the important idea or pattern.
- Start with a simple approach.
- Discuss optimized approaches when appropriate.
- Provide C++ code.
- Explain the code step by step.
- Always explain time complexity.
- Always explain space complexity.
- Encourage the student to think before giving the solution.
""",

    "Debugging": """
You are an expert C++ debugging tutor.

Your goal is to teach students how to find and fix bugs.

Rules:
- Carefully analyze the student's code.
- Identify syntax errors.
- Identify logical errors.
- Identify runtime errors.
- Identify conceptual mistakes.
- Explain why the error occurs.
- Show corrected code.
- Explain every important correction.
- Do not change working code unnecessarily.
"""
}


# ============================================================
# QUICK TOPICS
# ============================================================

QUICK_TOPICS = {

    "C++ Basics":
        "Teach me the fundamentals of C++ from the beginning.",

    "Arrays":
        "Teach me C++ arrays with examples and common interview problems.",

    "Strings":
        "Teach me strings in C++ from basics to common problems.",

    "Linked Lists":
        "Teach me linked lists in C++ with diagrams, implementation, and examples.",

    "OOP":
        "Teach me Object Oriented Programming in C++ with practical examples.",

    "Sorting":
        "Teach me sorting algorithms in C++ and explain their time complexities.",

    "Searching":
        "Teach me linear search and binary search in C++ with examples.",

    "Recursion":
        "Teach me recursion in C++ from beginner level with simple examples.",

    "DSA":
        "Give me a structured introduction to Data Structures and Algorithms in C++."
}


# ============================================================
# LEARNING ROADMAP
# ============================================================

LEARNING_ROADMAP = {

    "01. C++ Basics": """
Teach me C++ basics from the beginning.

Cover these topics in order:

1. What is C++?
2. Basic program structure
3. #include
4. main()
5. cout and cin
6. Variables
7. Data types
8. Operators
9. Type casting
10. Conditional statements
11. Loops
12. Functions

Teach one concept at a time.

Start with the first concept instead of overwhelming me.
""",

    "02. Arrays": """
Teach me arrays in C++ step by step.

Cover:

1. What is an array?
2. Declaration
3. Initialization
4. Accessing elements
5. Traversal
6. Input and output
7. Updating elements
8. Finding maximum and minimum
9. Searching
10. Common interview problems

Start from the basics.
""",

    "03. Strings": """
Teach me strings in C++ step by step.

Cover:

1. Character arrays
2. std::string
3. String input
4. String traversal
5. String functions
6. String manipulation
7. Character operations
8. Common interview problems

Start from beginner level.
""",

    "04. Linked Lists": """
Teach me linked lists in C++ from the beginning.

Cover:

1. What is a linked list?
2. Node
3. Head
4. Traversal
5. Insertion
6. Deletion
7. Searching
8. Singly linked list
9. Doubly linked list
10. Circular linked list

Explain with diagrams and C++ code.
Start with the first concept.
""",

    "05. Stack & Queue": """
Teach me Stack and Queue in C++.

Cover:

1. Stack
2. LIFO
3. Stack implementation
4. Stack operations
5. Queue
6. FIFO
7. Queue implementation
8. Queue operations
9. Deque
10. Applications
11. Common problems

Use simple examples.
""",

    "06. OOP": """
Teach me Object Oriented Programming in C++.

Cover:

1. Class
2. Object
3. Access modifiers
4. Constructor
5. Destructor
6. this pointer
7. Encapsulation
8. Inheritance
9. Polymorphism
10. Abstraction

Explain every concept with practical C++ examples.
""",

    "07. Recursion": """
Teach me recursion in C++.

Cover:

1. What is recursion?
2. Base case
3. Recursive case
4. Call stack
5. Factorial
6. Fibonacci
7. Sum problems
8. Array problems
9. String problems
10. Backtracking introduction

Explain execution step by step.
""",

    "08. Sorting": """
Teach me sorting algorithms in C++.

Cover:

1. Bubble Sort
2. Selection Sort
3. Insertion Sort
4. Merge Sort
5. Quick Sort

For each algorithm explain:

- Basic idea
- Example
- Step-by-step execution
- C++ implementation
- Time complexity
- Space complexity

Start with Bubble Sort.
""",

    "09. Searching": """
Teach me searching algorithms in C++.

Cover:

1. Linear Search
2. Binary Search
3. Conditions for Binary Search
4. Iterative Binary Search
5. Recursive Binary Search
6. Common interview problems

Start with Linear Search.
""",

    "10. Trees": """
Teach me Trees in C++ from beginner level.

Cover:

1. Tree terminology
2. Binary Tree
3. Tree Node
4. Preorder
5. Inorder
6. Postorder
7. Level Order
8. Binary Search Tree
9. BST insertion
10. BST searching
11. BST deletion

Explain visually where possible.
""",

    "11. Graphs": """
Teach me Graphs in C++ from the beginning.

Cover:

1. Vertices
2. Edges
3. Directed Graph
4. Undirected Graph
5. Weighted Graph
6. Adjacency Matrix
7. Adjacency List
8. BFS
9. DFS
10. Common graph problems

Start from the absolute basics.
""",

    "12. Dynamic Programming": """
Teach me Dynamic Programming in C++ from beginner level.

First explain:

1. What is Dynamic Programming?
2. Overlapping Subproblems
3. Optimal Substructure
4. Recursion
5. Memoization
6. Tabulation

Then gradually introduce classic DP problems.

Do not assume that I already understand DP.
"""
}


# ============================================================
# CREATE GEMINI CHAT
# ============================================================

def create_chat(client, mode):

    return client.chats.create(
        model="gemini-3.6-flash",
        config={
            "system_instruction": TUTOR_MODES[mode]
        }
    )


# ============================================================
# SESSION STATE
# ============================================================

if "mode" not in st.session_state:
    st.session_state.mode = "Beginner"


if "chat" not in st.session_state:
    st.session_state.chat = create_chat(
        client,
        st.session_state.mode
    )


if "messages" not in st.session_state:
    st.session_state.messages = []


if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


# ============================================================
# CURRENT LESSON
# ============================================================

if "current_topic" not in st.session_state:
    st.session_state.current_topic = None


# ============================================================
# PROGRESS
# ============================================================

if "completed_topics" not in st.session_state:
    st.session_state.completed_topics = set()


# ============================================================
# REQUEST PROTECTION
# ============================================================

if "last_request_time" not in st.session_state:
    st.session_state.last_request_time = 0


if "request_count" not in st.session_state:
    st.session_state.request_count = 0


MAX_SESSION_REQUESTS = 30
REQUEST_COOLDOWN = 5


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_progress():

    total_topics = len(LEARNING_ROADMAP)

    completed_topics = len(
        st.session_state.completed_topics
    )

    if total_topics == 0:
        return 0

    return int(
        (completed_topics / total_topics) * 100
    )


def mark_current_topic_complete():

    if st.session_state.current_topic:

        st.session_state.completed_topics.add(
            st.session_state.current_topic
        )


# ============================================================
# HEADER
# ============================================================

st.title("🤖 C++ AI Tutor")

st.caption(
    "Learn C++, DSA, algorithms, debugging, and programming with AI."
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Settings")


    # ========================================================
    # TUTOR MODE
    # ========================================================

    selected_mode = st.selectbox(
        "Tutor Mode",
        list(TUTOR_MODES.keys()),
        index=list(TUTOR_MODES.keys()).index(
            st.session_state.mode
        )
    )


    # ========================================================
    # CHANGE TUTOR MODE
    # ========================================================

    if selected_mode != st.session_state.mode:

        st.session_state.mode = selected_mode

        st.session_state.chat = create_chat(
            client,
            selected_mode
        )

        st.session_state.messages = []

        st.rerun()


    st.divider()


    # ========================================================
    # QUICK TOPICS
    # ========================================================

    st.header("🚀 Quick Topics")

    for topic, topic_prompt in QUICK_TOPICS.items():

        if st.button(
            topic,
            use_container_width=True
        ):

            st.session_state.pending_prompt = topic_prompt

            st.rerun()


    st.divider()


    # ========================================================
    # LEARNING ROADMAP
    # ========================================================

    st.header("📚 Learning Roadmap")

    for topic, topic_prompt in LEARNING_ROADMAP.items():

        if st.button(
            topic,
            use_container_width=True
        ):

            st.session_state.current_topic = topic

            st.session_state.pending_prompt = topic_prompt

            st.rerun()


    st.divider()


    # ========================================================
    # PROGRESS
    # ========================================================

    st.subheader("📊 Learning Progress")

    progress = get_progress()

    st.progress(
        progress / 100
    )

    st.write(
        f"**{progress}% complete**"
    )

    st.write(
        f"{len(st.session_state.completed_topics)} "
        f"of {len(LEARNING_ROADMAP)} topics completed"
    )


    # ========================================================
    # COMPLETED TOPICS
    # ========================================================

    if st.session_state.completed_topics:

        st.write("### ✅ Completed")

        for topic in LEARNING_ROADMAP:

            if topic in st.session_state.completed_topics:

                st.write(
                    f"✅ {topic}"
                )


    st.divider()


    # ========================================================
    # SESSION USAGE
    # ========================================================

    st.subheader("📊 Session Usage")

    st.write(
        f"Requests used: "
        f"{st.session_state.request_count}/"
        f"{MAX_SESSION_REQUESTS}"
    )


    st.divider()


    # ========================================================
    # ABOUT
    # ========================================================

    st.subheader("About")

    st.write(
        "A Gemini-powered C++ tutor designed to help "
        "you learn programming through explanations, "
        "examples, DSA practice, interviews, and debugging."
    )


    st.divider()


    # ========================================================
    # CLEAR CONVERSATION
    # ========================================================

    if st.button(
        "🗑️ Clear conversation",
        use_container_width=True
    ):

        st.session_state.chat = create_chat(
            client,
            st.session_state.mode
        )

        st.session_state.messages = []

        st.rerun()


# ============================================================
# CURRENT TUTOR MODE
# ============================================================

st.info(
    f"Current tutor mode: **{st.session_state.mode}**"
)


# ============================================================
# CURRENT LESSON
# ============================================================

if st.session_state.current_topic:

    st.subheader(
        f"📖 Current Lesson: {st.session_state.current_topic}"
    )

    if (
        st.session_state.current_topic
        in st.session_state.completed_topics
    ):

        st.success(
            "✅ This topic is completed!"
        )

    else:

        st.write(
            "Study this topic and mark it complete when "
            "you are comfortable with the concepts."
        )

        if st.button(
            "✅ Mark Topic Complete",
            use_container_width=True
        ):

            mark_current_topic_complete()

            st.success(
                f"{st.session_state.current_topic} "
                "marked as completed!"
            )

            st.rerun()


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ============================================================
# GET QUICK TOPIC / ROADMAP PROMPT
# ============================================================

prompt = st.session_state.pop(
    "pending_prompt",
    None
)


# ============================================================
# NORMAL CHAT INPUT
# ============================================================

user_prompt = st.chat_input(
    "Ask me a C++ question..."
)


if user_prompt:

    prompt = user_prompt


# ============================================================
# PROCESS MESSAGE
# ============================================================

if prompt:

    # ========================================================
    # SESSION REQUEST LIMIT
    # ========================================================

    if (
        st.session_state.request_count
        >= MAX_SESSION_REQUESTS
    ):

        st.warning(
            "⚠️ You have reached the request limit "
            "for this session. Please start a new session later."
        )

        st.stop()


    # ========================================================
    # REQUEST COOLDOWN
    # ========================================================

    current_time = time.time()

    time_since_last_request = (
        current_time
        - st.session_state.last_request_time
    )


    if (
        st.session_state.last_request_time > 0
        and time_since_last_request < REQUEST_COOLDOWN
    ):

        remaining = int(
            REQUEST_COOLDOWN
            - time_since_last_request
        ) + 1


        st.warning(
            f"⏳ Please wait {remaining} seconds "
            "before sending another question."
        )

        st.stop()


    # ========================================================
    # UPDATE REQUEST COUNTER
    # ========================================================

    st.session_state.last_request_time = current_time

    st.session_state.request_count += 1


    # ========================================================
    # DISPLAY USER MESSAGE
    # ========================================================

    with st.chat_message("user"):

        st.markdown(prompt)


    # ========================================================
    # SAVE USER MESSAGE
    # ========================================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )


    # ========================================================
    # GENERATE GEMINI RESPONSE
    # ========================================================

    with st.chat_message("assistant"):

        try:

            response_stream = (
                st.session_state.chat.send_message_stream(
                    prompt
                )
            )


            answer = st.write_stream(
                chunk.text
                for chunk in response_stream
                if chunk.text
            )


            # ==================================================
            # SAVE AI RESPONSE
            # ==================================================

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


        except Exception as e:

            error_message = str(e)


            # ==================================================
            # QUOTA ERROR
            # ==================================================

            if (
                "429" in error_message
                or "RESOURCE_EXHAUSTED" in error_message
            ):

                st.warning(
                    "⚠️ Gemini's API quota has been "
                    "temporarily reached. Please try again later."
                )


            # ==================================================
            # OTHER ERROR
            # ==================================================

            else:

                st.error(
                    "Sorry, I couldn't process your request."
                )

                st.caption(
                    "Please try again or check the "
                    "application configuration."
                )