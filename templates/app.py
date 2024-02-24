from flask import Flask, request, jsonify
import mysql.connector as connection
import pymongo

app = Flask(__name__)


def sql_table_queries(op, name, values,  col1=None, col2=None, val1=None, val2=None):
    if op.lower() == "tablecreation":
        query = f'CREATE TABLE {name} (ID INT(10), Name VARCHAR(20), GENDER VARCHAR(10), AGE INT(10))'
        return query, values


    elif op.lower() == "insertion":
        query = f'INSERT INTO {name} (ID, Name, GENDER, AGE) VALUES (%s, %s, %s, %s)'
        return query, values

    elif op.lower() == "deletion":
        query = f'DROP TABLE {name}'
        return query, values

    elif op.lower() == "update":
        query = f'UPDATE {name} SET {col1} = %s WHERE {col2} = %s'
        values = (val1, val2)
        return query, values


def perform_sqldb_operation(db_operation, op, table_name, values=None, col1=None, col2=None, val1=None, val2=None):
    try:
        if db_operation.lower() == "sql":
            conn = connection.connect(host="localhost", user="root", passwd="mysql123", database='razer', use_pure=True)
            cursor = conn.cursor()
            query, values = sql_table_queries(op, table_name, values, col1, col2, val1, val2)
            if op.lower() == 'insertion':
                if len(values) > 1:
                    cursor.executemany(query, values)
                else:
                    cursor.execute(query, values[0])
            else:
                cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
            return 'SQL operation executed successfully.'
    except Exception as e:
        return str(e)


def perform_MongoDB_operation(op, dbname, collname, values):
    try:
        client = pymongo.MongoClient("mongodb+srv://chiragpattanaik03:mysql123@atlascluster.qkrcncj.mongodb.net/?retryWrites=true&w=majority")
        db = client[dbname]  # created a database in the mongodb
        if op == "collectioncreation":
            db[collname]  # created a collection in the mongoDB database
            return {"message": f"Collection '{collname}' accessed or created in database '{dbname}'."}

        if op == "insertion":
            if len(values) > 1:
                db[collname].insert_many(values)
            else:
                db[collname].insert_one(values[0])
            return {"message": f"Records has been inserted in the database '{dbname}"}

        if op == "deletion":
            db[collname].delete_many({})  # To delete all the records from the collection
            return {"message": f"Records has been deleted from the database '{dbname}"}

    except Exception as e:
        print(str(e))


@app.route('/sql', methods=['POST'])
def choose_db():
    try:
        if request.method == 'POST':
            data = request.get_json()
            operation = request.json['operation']
            op_perform = request.json['op']
            column1 = request.json['col1']
            column2 = request.json['col2']
            value1 = request.json['val1']
            value2 = request.json['val2']
            values = data.get('values')
            Tablename = request.json['tablename']

            if op_perform.lower() == 'update':
                result = perform_sqldb_operation(operation, op_perform, Tablename, values, column1, column2, value1, value2)
            else:
                result = perform_sqldb_operation(operation, op_perform, Tablename, values)

            return jsonify(result=result)
    except Exception as e:
        print(str(e))
        return jsonify(error=str(e)), 500


@app.route('/MongoDB', methods=['POST'])
def choose_mongodb():
    try:
        if request.method == 'POST':
            data = request.get_json()
            operation = request.json['op']
            dbname = request.json['dbname']
            collname = request.json['nameofcoll']
            values = data.get('val')
            result = perform_MongoDB_operation(operation, dbname, collname, values)
            return jsonify(result=result)

    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    app.run(debug=True)

# {
#   "op": "insertion",
#   "dbname": "APiDB",
#   "nameofcoll":"APi_collection_DB",
#   "val": [{"companyName": "iNeuron",
#          "product": "Affordable AI",
#          "courseOfferedl": "Deep Learning for Computer Vision",
#         "name": ["sudhanshu","kumar",5466],
#          "record_dict": {"name":"sudhanshu","occupation":"tutor","Age":26}},
#          {"companyName": "iNeuron",
#          "product": "Affordable AI",
#          "courseOfferedl": "Deep Learning for Computer Vision",
#         "name": ["chirag","pattanaik",9864543],
#          "record_dict": {"name":"chiragpattanaik","occupation":"student","Age":20}}]
# }
