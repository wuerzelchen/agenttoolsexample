import os
import requests
from flask import Flask, render_template, jsonify
from identity.flask import Auth
import app_config
from langchain_openai import AzureChatOpenAI
from tools.machine import wrap_machine_api
from langgraph.prebuilt import create_react_agent

app = Flask(__name__)
app.config.from_object(app_config)

auth = Auth(
    app,
    authority=app.config["AUTHORITY"],
    client_id=app.config["CLIENT_ID"],
    client_credential=app.config["CLIENT_SECRET"],
    redirect_uri=app.config["REDIRECT_URI"]
)


@app.route("/")
@auth.login_required
def index(*, context):
    return render_template(
        'index.html',
        user=context['user'],
        title="LLM Tools Sample",
    )

# backend api call from server http://localhost:8085/get_info


@app.route("/api/get_info")
@auth.login_required(scopes=["api://332551fa-2cc8-4511-8e9c-cfbaf9451565/.default"])
def get_info(*, context):
    if context.get('access_token'):
        api_result = requests.get(
            os.getenv("ENDPOINT"),
            headers={'Authorization': 'Bearer ' + context['access_token']},
            timeout=30,
        ).json()
        return jsonify(api_result)
    else:
        return jsonify({"error": "Did you forget to set the SCOPE environment variable?"}), 400

# create a route for the llm call to https://admin-m34emcnx-swedencentral.openai.azure.com/ with the deployment name "gpt-4o"


@app.route("/api/llm")
@auth.login_required(scopes=[app.config["LLM_SCOPE"]])
def llm(*, context):
    model = AzureChatOpenAI(
        azure_endpoint=app.config["AZURE_OPENAI_ENDPOINT"],
        openai_api_version=app.config["AZURE_OPENAI_API_VERSION"],
        deployment_name=app.config["AZURE_OPENAI_DEPLOYMENT_NAME"],
        openai_api_type="azure",
        azure_ad_token=context['access_token']
    )
    chat_prompt = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "You are a helpful machine assistant. You give information about machines in a factory."
                }
            ]
        }
    ]
    machine_api = wrap_machine_api(
        {
            "access_token": context['access_token'],
            "endpoint": app.config["ENDPOINT"]
        }
    )
    tools = [machine_api]
    agent = create_react_agent(
        model=model,
        tools=tools,
        prompt="You are a helpful machine assistant. You give information about machines in a factory.",
    )
    output = agent.invoke(
        {"messages": [{"role": "user", "content": "List all IDs of machines which are in running state."}]})
    # Defensive: try to get the content, fallback to str(output)
    try:
        result = output['messages'][3].content
    except Exception:
        result = str(output)
    return jsonify({"result": result})
