import { useEffect, useState } from "react";
import "./App.css";

function App() {

  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = () => {
    fetch("http://127.0.0.1:5000/tasks")
      .then(res => res.json())
      .then(data => setTasks(data));
  };

  const addTask = () => {

    if(title==="") return;

    fetch("http://127.0.0.1:5000/tasks",{

      method:"POST",

      headers:{
        "Content-Type":"application/json"
      },

      body:JSON.stringify({
        title:title
      })

    }).then(()=>{
      setTitle("");
      fetchTasks();
    });

  };

  const deleteTask=(id)=>{

    fetch(`http://127.0.0.1:5000/tasks/${id}`,{

      method:"DELETE"

    }).then(()=>{
      fetchTasks();
    });

  };

  const completeTask=(task)=>{

    fetch(`http://127.0.0.1:5000/tasks/${task.id}`,{

      method:"PUT",

      headers:{
        "Content-Type":"application/json"
      },

      body:JSON.stringify({

        title:task.title,
        status:"Completed"

      })

    }).then(()=>{
      fetchTasks();
    });

  };

  return (

    <div className="container">

      <h1>Task Manager</h1>

      <div className="addTask">

        <input

          type="text"

          placeholder="Enter Task"

          value={title}

          onChange={(e)=>setTitle(e.target.value)}

        />

        <button onClick={addTask}>
          Add
        </button>

      </div>

      <table>

        <thead>

          <tr>

            <th>ID</th>
            <th>Title</th>
            <th>Status</th>
            <th>Action</th>

          </tr>

        </thead>

        <tbody>

        {

          tasks.map(task=>(

            <tr key={task.id}>

              <td>{task.id}</td>

              <td>{task.title}</td>

              <td>{task.status}</td>

              <td>

                <button
                onClick={()=>completeTask(task)}>
                  Complete
                </button>

                <button
                onClick={()=>deleteTask(task.id)}>
                  Delete
                </button>

              </td>

            </tr>

          ))

        }

        </tbody>

      </table>

    </div>

  );

}

export default App;