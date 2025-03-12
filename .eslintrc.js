module.exports = {
    env: {
        browser: true,
        es2021: true,
    },
    extends: ['react-app', 'airbnb', 'prettier'],
    plugins: ['react', 'prettier'],
    rules: {
        'prettier/prettier': 'error', // Displays Prettier errors as ESLint errors
        'react/jsx-filename-extension': [1, { extensions: ['.js', '.jsx'] }],
        'no-unused-vars': 'warn',
        'react/react-in-jsx-scope': 'off',
        'no-console': 'warn',
        'default-param-last': 'off',
        'no-param-reassign': [
            'error',
            {
                props: true,
                ignorePropertyModificationsFor: ['state', 'draft'],
            },
        ],
    },
    overrides: [
        {
            env: {
                node: true,
            },
            files: ['**/*.test.js', '**/*.test.jsx', 'src/setupTests.js'],
            rules: {
                'import/no-extraneous-dependencies': [
                    'error',
                    { devDependencies: true },
                ],
            },
        },
    ],
    parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
    },
};
