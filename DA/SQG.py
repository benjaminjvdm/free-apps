import streamlit as st
from sqlglot import parse_one, exp
import networkx as nx
import matplotlib.pyplot as plt

st.title("SQL Query Builder")

# Function to generate the query string
def generate_query(components):
    query_components = [
        f"SELECT {', '.join(components['columns'])}",
        f"FROM {components['tables']}",
        f"WHERE {components['where']}" if components['where'] else "",
        f"GROUP BY {components['group_by']}" if components['group_by'] else "",
        f"HAVING {components['having']}" if components['having'] else "",
        f"ORDER BY {components['order_by']}" if components['order_by'] else "",
        f"LIMIT {components['limit']}" if components['limit'] else ""
    ]
    return " \n".join(query_components)

# Sidebar with Query Components (using a dictionary for better organization)
with st.sidebar:
    st.subheader("Query Components")
    components = {
        "tables": st.text_input("Tables (comma-separated)", "employees, departments"),
        "columns": st.multiselect("Columns (select multiple)", ["*"], ["*"]),  # Default to '*'
        "where": st.text_area("WHERE Clause", "salary > 50000"),
        "group_by": st.text_input("GROUP BY", "department_id"),
        "having": st.text_input("HAVING", "COUNT(*) > 10"),
        "order_by": st.text_input("ORDER BY", "salary DESC"),
        "limit": st.number_input("LIMIT", min_value=0, value=10)
    }

# Main Area for Query Generation and Visualization
st.subheader("Generated Query")
query = generate_query(components)
st.code(query, language="sql")

# Query Visualization
st.subheader("Query Visualization")
try:
    parsed_query = parse_one(query)

    # Enhanced Graph Creation
    G = nx.DiGraph()
    for table in parsed_query.find_all(exp.Table):
        G.add_node(table.name)
    for join in parsed_query.find_all(exp.Join):
        if join.this and join.expression:  # Ensure both sides of the join are valid
            G.add_edge(join.this.name, join.expression.name)
        else:
            st.warning(f"Invalid join condition detected: {join}")

    # Enhanced Graph Drawing (using a circular layout)
    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=3000, node_color='skyblue', font_size=12, arrowsize=20)
    plt.title("Table Relationships")
    st.pyplot(plt.gcf())

except Exception as e:
    st.error(f"Error parsing the query: {e}")
