
"use client";

import React, { useState, useEffect } from "react";

// Individual task item component
const TaskItem = ({ task, onToggleComplete, onDelete }) => {
  return (
    <div
      style={{ display: "flex", alignItems: "center", marginBottom: "10px" }}
    >
      <input
        type="checkbox"
        checked={task.completed}
        onChange={() => onToggleComplete(task.id)}
        style={{ marginRight: "10px" }}
      />
      <span
        style={{
          textDecoration: task.completed ? "line-through" : "none",
          flex: 1,
        }}
      >
        {task.name}
      </span>
      <button onClick={() => onDelete(task.id)} style={{ marginLeft: "10px" }}>
        Delete
      </button>
    </div>
  );
};

// Main TaskManager component
const TaskManager = () => {
  const [tasks, setTasks] = useState([]);
  const [newTaskName, setNewTaskName] = useState("");
  const [filter, setFilter] = useState("all");
  const [taskIdCounter, setTaskIdCounter] = useState(1);

  // Handle task input change
  const handleInputChange = (e) => {
    setNewTaskName(e.target.value);
  };

  // Add a new task
  const addTask = () => {
    if (newTaskName.trim()) {
      const newTask = {
        id: taskIdCounter,
        name: newTaskName,
        completed: false,
      };
      setTasks([...tasks, newTask]);
      setNewTaskName("");
      setTaskIdCounter(taskIdCounter + 1);
    }
  };

  // Toggle task completion
  const toggleTaskCompletion = (id) => {
    setTasks(
      tasks.map((task) =>
        task.id === id ? { ...task, completed: !task.completed } : task,
      ),
    );
  };

  // Delete task
  const deleteTask = (id) => {
    setTasks(tasks.filter((task) => task.id !== id));
  };

  // Filter tasks based on the selected filter
  const getFilteredTasks = () => {
    switch (filter) {
      case "completed":
        return tasks.filter((task) => task.completed);
      case "incomplete":
        return tasks.filter((task) => !task.completed);
      default:
        return tasks;
    }
  };

  // Handle filter change
  const handleFilterChange = (e) => {
    setFilter(e.target.value);
  };

  // Effect hook to log tasks (as an example)
  useEffect(() => {
    console.log("Current tasks:", tasks);
  }, [tasks]);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Task Manager</h1>

      {/* Input and button to add tasks */}
      <div style={{ marginBottom: "20px" }}>
        <input
          type="text"
          value={newTaskName}
          onChange={handleInputChange}
          placeholder="Enter new task"
          style={{ padding: "10px", width: "300px", marginRight: "10px" }}
        />
        <button onClick={addTask} style={{ padding: "10px" }}>
          Add Task
        </button>
      </div>

      {/* Filter options */}
      <div style={{ marginBottom: "20px" }}>
        <label style={{ marginRight: "10px" }}>Filter: </label>
        <select value={filter} onChange={handleFilterChange}>
          <option value="all">All</option>
          <option value="completed">Completed</option>
          <option value="incomplete">Incomplete</option>
        </select>
      </div>

      {/* Task List */}
      <div>
        {getFilteredTasks().map((task) => (
          <TaskItem
            key={task.id}
            task={task}
            onToggleComplete={toggleTaskCompletion}
            onDelete={deleteTask}
          />
        ))}
      </div>
    </div>
  );
};

export default TaskManager;
