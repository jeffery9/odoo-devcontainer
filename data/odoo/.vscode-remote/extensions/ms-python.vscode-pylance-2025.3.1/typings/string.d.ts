/**
 * This file is used to declare global types and interfaces that are not part of the standard TypeScript. It's repeated
 * in multiple packages to ensure that the types are available in all packages.
 */
export {};

declare global {
    // https://stackoverflow.com/questions/39877156/how-to-extend-string-prototype-and-use-it-next-in-typescript
    // eslint-disable-next-line @typescript-eslint/naming-convention, @typescript-eslint/no-unused-vars
    interface String {
        /**
         * Split a string using the cr and lf characters and return them as an array.
         * By default lines are trimmed and empty lines are removed.
         * @param {SplitLinesOptions=} splitOptions - Options used for splitting the string.
         */
        splitLines(splitOptions?: { trim: boolean; removeEmptyEntries?: boolean }): string[];
        /**
         * Appropriately formats a string so it can be used as an argument for a command in a shell.
         * E.g. if an argument contains a space, then it will be enclosed within double quotes.
         */
        toCommandArgument(): string;
        /**
         * Appropriately formats a a file path so it can be used as an argument for a command in a shell.
         * E.g. if an argument contains a space, then it will be enclosed within double quotes.
         */
        fileToCommandArgument(): string;
        /**
         * String.format() implementation.
         * Tokens such as {0}, {1} will be replaced with corresponding positional arguments.
         */
        format(...args: string[]): string;

        /**
         * String.trimQuotes implementation
         * Removes leading and trailing quotes from a string
         */
        trimQuotes(): string;
    }
}
