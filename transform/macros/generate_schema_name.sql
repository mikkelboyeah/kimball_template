{% macro generate_schema_name(custom_schema_name, node) -%}

    {%- set default_schema = target.schema -%}
    
    {%- if custom_schema_name is none -%}
        {{ default_schema }}
    {%- else -%}
        {%- if target.name == 'prod' -%}
            {{ custom_schema_name | trim }}
        {%- else -%}
            {%- set user = env_var('USER', env_var('USERNAME', 'dev')) -%}
            z_{{ user }}_{{ custom_schema_name | trim }}
        {%- endif -%}
    {%- endif -%}

{%- endmacro %}
