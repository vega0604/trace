
const tasks = new Set([
    {
        id: 1, 
        title: 'Design new landing page',
        description: 'Create a new landing page for our upcoming product launch.',
        tags: ['design', 'marketing'],
        dependencies: [],
        assignedTo: [3, 4], // Mikaela Olarte and Rita Zhang
        status: 'in progress',
        createdAt: '2024-06-01',
        updatedAt: '2024-06-10',
        dueDate: '2024-07-15'
    },
    {
        id: 2, 
        title: 'Develop new landing page',
        description: 'Create a new landing page for our upcoming product launch.',
        tags: ['design', 'marketing'],
        dependencies: [1], // Depends on the design task
        assignedTo: [3, 4], // Mikaela Olarte and Rita Zhang
        status: 'blocked',
        createdAt: '2024-06-01',
        updatedAt: '2024-06-10',
        dueDate: '2024-07-15'
    },
    { 
        id: 3,
        title: 'Implement user authentication',
        description: 'Develop a secure user authentication system for our web application.',
        tags: ['development', 'security'],
        dependencies: [],
        assignedTo: [1, 2], // Sebastian Vega and Diego Pachas
        status: 'not started',
        createdAt: '2024-06-05',
        updatedAt: '2024-06-05',
        dueDate: '2024-07-30'
    }
]);

export default tasks;