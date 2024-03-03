/* eslint-disable func-names */
import dayjs from 'dayjs';
import 'dayjs/locale/de-ch';
import utc from 'dayjs/plugin/utc';
import duration from 'dayjs/plugin/duration';
import relativeTime from 'dayjs/plugin/relativeTime';
import timezone from 'dayjs/plugin/timezone';

dayjs.extend(utc);
dayjs.extend(duration);
dayjs.extend(relativeTime);
dayjs.extend(timezone);
dayjs.locale('de-ch')
dayjs.tz.setDefault('Europe/Zurich');

export default dayjs;