import streamlit as st
from sqlglot import parse_one, exp
from sqlglot.dialects import to_sql  # Correct import for to_sql
import networkx as nx
import matplotlib.pyplot as plt

# Rest of the code is the same as before

# Function to generate the query string
def generate_query(components, join_options):
    query_parts = []
    query_parts.append(f"SELECT {', '.join(selected_columns)}")
    query_parts.append(f"FROM {tables}")
    for join in join_options:
        if join["type"] and join["table"] and join["on"]:
            query_parts.append(f"{join['type']} JOIN {join['table']} ON {join['on']}")
    if where_conditions:
        query_parts.append(f"WHERE {where_conditions}")
    if group_by_columns:
        query_parts.append(f"GROUP BY {group_by_columns}")
    if having_conditions:
        query_parts.append(f"HAVING {having_conditions}")
    if order_by_columns:
        query_parts.append(f"ORDER BY {order_by_columns}")
    if limit_value:
        query_parts.append(f"LIMIT {limit_value}")
        
    return " ".join(query_parts)


# Display Query
st.subheader("Generated Query")
query = generate_query(components, join_options)
st.code(query, language="sql")

# Visualize Query (if possible)
st.subheader("Query Visualization")
if query:
    try:
        parsed_query = parse_one(query)

        G = nx.DiGraph()
        # Add nodes for tables and subqueries
        for table in parsed_query.find_all(exp.Table):
            G.add_node(table.name, type="table")
        for subquery in parsed_query.find_all(exp.Subquery):
            G.add_node(subquery.alias or "Subquery", type="subquery")
        # Add edges for joins
        for join in parsed_query.find_all(exp.Join):
            this_table = join.this.name if isinstance(join.this, exp.Table) else join.this.alias or "Subquery"
            joined_table = join.expression.name if isinstance(join.expression, exp.Table) else join.expression.alias or "Subquery"
            G.add_edge(this_table, joined_table, label=join.side)
        # Add edges for subquery references
        for subquery in parsed_query.find_all(exp.Subquery):
            for table in subquery.find_all(exp.Table):
                G.add_edge(subquery.alias or "Subquery", table.name)
        # Add nodes for functions (optional)
        for func in parsed_query.find_all(exp.Func):
            G.add_node(func.name, type="function")
            for arg in func.args:
                if isinstance(arg, exp.Column):
                    table_name = arg.table or parsed_query.find(exp.Table).name
                    G.add_edge(func.name, table_name)
        # Draw the graph
        pos = nx.spring_layout(G)
        node_colors = {
            "table": "skyblue", 
            "subquery": "lightgreen", 
            "function": "orange"
        }
        edge_colors = {
            "left": "blue", 
            "right": "red", 
            "inner": "black", 
            "outer": "purple", 
            "cross": "yellow"
        }
        nx.draw(
            G, 
            pos, 
            with_labels=True, 
            font_weight='bold', 
            node_size=3000, 
            node_color=[node_colors.get(G.nodes[n]["type"], "gray") for n in G.nodes],
            edge_color=[edge_colors.get(G[u][v].get("label", ""), "gray") for u, v in G.edges],
            font_size=12, 
            arrowsize=20
        )
        edge_labels = {(u, v): d["label"] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
        plt.title("Query Visualization")
        st.pyplot(plt.gcf())

    except Exception as e:
        st.error(f"Error parsing the query: {e}")
