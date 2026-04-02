streamlit.errors.StreamlitMixedNumericTypesError: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).

Traceback:
File "/mount/src/chaosforge/app.py", line 95, in <module>
    avg = st.number_input("Avg monthly spend $", value=default_avg[i], min_value=0.0, key=f"avg_{i}")
File "/home/adminuser/venv/lib/python3.14/site-packages/streamlit/runtime/metrics_util.py", line 563, in wrapped_func
    result = non_optional_func(*args, **kwargs)
File "/home/adminuser/venv/lib/python3.14/site-packages/streamlit/elements/widgets/number_input.py", line 447, in number_input
    return self._number_input(
           ~~~~~~~~~~~~~~~~~~^
        label=label,
        ^^^^^^^^^^^^
    ...<16 lines>...
        ctx=ctx,
        ^^^^^^^^
    )
    ^
File "/home/adminuser/venv/lib/python3.14/site-packages/streamlit/elements/widgets/number_input.py", line 530, in _number_input
    raise StreamlitMixedNumericTypesError(
        value=value, min_value=min_value, max_value=max_value, step=step
    )
