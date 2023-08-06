/**
 * Parse a date string.
 *
 * Expected formats: DateFormat TimeFormat TimezoneFormat
 * - DateFormats:
 *   - YYYY-MM, YYYY-MM-DD, YYYY-M, YYYY-M-D
 *   - MM/YYYY, MM/DD/YYYY, M/YYYY, M/D/YYYY
 * - TimeFormats:
 *   - HH:MM, HH:MM:SS
 *   - HH:MM{am/pm}, HH:MM:SS{am/pm}
 * - TimezoneFormat:
 *   - +HH:MM, -HH:MM
 *
 * If no timezone is specified, UTC is assumed
 *
 * @param str the date string
 * @returns the parsed Date's unix timestamp (in milliseconds) or null if unable to parse
 */
export declare function parseDate(str: string, timeZoneOffsetMinutes?: number): number;
export declare const defaultDateTimeFormat = "%m/%d/%Y %H:%M:%S";
/** Returns format for given string of date */
export declare function getDateFormat(str: string): string;
export declare const monthNames: string[];
/** Check if a string is a month name, if yes, return a normalized version */
export declare function testAndNormalizeMonthName(str: string): string;
