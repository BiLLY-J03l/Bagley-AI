from openai import OpenAI
import argparse

#insert OpenAI API here
API_KEY=""

bagley=OpenAI(
    api_key=API_KEY
)

def get_opts():
    parser=argparse.ArgumentParser()
    parser.add_argument("-i","--interactive",action="store_true",help="Interactive Session with Bagley")
    parser.add_argument("query",type=str,nargs="?",help="The query you want Bagley to help you with")
    options=parser.parse_args()
   
    if not options.interactive:
        #NOT INTERACTIVE SESSION    
        global query
        query=options.query
        return 1
        
    else:
        #INTERACTIVE SESSION
        return 2
   
def YES_Interactive():
    try:
        chat_log=[]
        while True:
            user_msg=input("[-] You: ")
            if user_msg.lower() == 'quit':
                print("[+] Bagley: Happy to help!!")
                exit(0)
            else:
                chat_log.append({"role": "user", "content": user_msg})
                stream = bagley.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=chat_log,
                        stream=True
                        )
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        print("[+] Bagley:",chunk.choices[0].delta.content, end="") 
    except Exception as e:
        print("[x] Error:",e)

def NO_Interactive():   
    try:
        stream = bagley.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": query}],
            stream=True
            )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")
    except Exception as e:
        print("[x] Error:",e)
    
if __name__ == "__main__":
    if get_opts() == 1 : 
        #print("NO INTERACTIVE")
        NO_Interactive()
    elif get_opts() == 2 :
        #print("YES INTERACTIVE")
        YES_Interactive()
    else:
        print("ERROR")
