from collections import defaultdict

class ChartData:
    @staticmethod
    def get_subject_averages(scores):
        """Calculate average scores per subject"""
        subject_scores = defaultdict(lambda: {'total': 0, 'count': 0})
        
        for score in scores:
            subject = score.quiz.chapter.subject.name
            percentage = (score.score / score.total_questions) * 100
            subject_scores[subject]['total'] += percentage
            subject_scores[subject]['count'] += 1
        
        # Calculate averages
        averages = {
            subject: data['total'] / data['count']
            for subject, data in subject_scores.items()
        }
        
        return {
            'labels': list(averages.keys()),
            'data': list(averages.values())
        }
    
    @staticmethod
    def get_score_distribution(scores):
        """Calculate score distribution in ranges"""
        ranges = {
            '90-100': 0,
            '80-89': 0,
            '70-79': 0,
            '60-69': 0,
            '0-59': 0
        }
        
        for score in scores:
            percentage = (score.score / score.total_questions) * 100
            if percentage >= 90:
                ranges['90-100'] += 1
            elif percentage >= 80:
                ranges['80-89'] += 1
            elif percentage >= 70:
                ranges['70-79'] += 1
            elif percentage >= 60:
                ranges['60-69'] += 1
            else:
                ranges['0-59'] += 1
        
        return {
            'labels': list(ranges.keys()),
            'data': list(ranges.values())
        }
    
    @staticmethod
    def format_chart_data(scores):
        """Format all chart data for template"""
        return {
            'subject_chart': ChartData.get_subject_averages(scores),
            'distribution_chart': ChartData.get_score_distribution(scores)
        }

    @staticmethod
    def get_subject_chart_config(subject_stats):
        """Generate bar chart config for subject-wise statistics"""
        return {
            'type': 'bar',
            'data': {
                'labels': subject_stats['labels'],
                'datasets': [{
                    'label': 'Number of Quizzes',
                    'data': subject_stats['data'],
                    'backgroundColor': [
                        'rgba(54, 162, 235, 0.5)',
                        'rgba(75, 192, 192, 0.5)',
                        'rgba(255, 99, 132, 0.5)'
                    ],
                    'borderColor': [
                        'rgba(54, 162, 235, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(255, 99, 132, 1)'
                    ],
                    'borderWidth': 1
                }]
            },
            'options': {
                'responsive': True,
                'scales': {
                    'y': {
                        'beginAtZero': True,
                        'ticks': {
                            'stepSize': 1
                        }
                    }
                }
            }
        }

    @staticmethod
    def get_month_chart_config(month_stats):
        """Generate pie chart config for month-wise statistics"""
        return {
            'type': 'pie',
            'data': {
                'labels': month_stats['labels'],
                'datasets': [{
                    'data': month_stats['data'],
                    'backgroundColor': [
                        'rgba(255, 99, 132, 0.5)',
                        'rgba(54, 162, 235, 0.5)',
                        'rgba(255, 206, 86, 0.5)'
                    ],
                    'borderColor': [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)'
                    ],
                    'borderWidth': 1
                }]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'legend': {
                        'position': 'bottom'
                    }
                }
            }
        }

    @staticmethod
    def get_admin_top_scores_config(subject_stats):
        """Generate bar chart config for admin top scores"""
        return {
            'type': 'bar',
            'data': {
                'labels': subject_stats['labels'],
                'datasets': [{
                    'label': 'Top Score (%)',
                    'data': subject_stats['scores'],
                    'backgroundColor': 'rgba(54, 162, 235, 0.5)',
                    'borderColor': 'rgba(54, 162, 235, 1)',
                    'borderWidth': 1
                }]
            },
            'options': {
                'responsive': True,
                'scales': {
                    'y': {
                        'beginAtZero': True,
                        'max': 100,
                        'title': {
                            'display': True,
                            'text': 'Score Percentage'
                        }
                    }
                }
            }
        }

    @staticmethod
    def get_admin_attempts_config(attempt_stats):
        """Generate doughnut chart config for admin user attempts"""
        return {
            'type': 'doughnut',
            'data': {
                'labels': attempt_stats['labels'],
                'datasets': [
                    {
                        'label': 'Total Users',
                        'data': [d[0] for d in attempt_stats['data']],
                        'backgroundColor': 'rgba(255, 206, 86, 0.5)',
                        'borderColor': 'rgba(255, 206, 86, 1)',
                        'borderWidth': 1
                    },
                    {
                        'label': 'Users who Attempted',
                        'data': [d[1] for d in attempt_stats['data']],
                        'backgroundColor': 'rgba(54, 162, 235, 0.5)',
                        'borderColor': 'rgba(54, 162, 235, 1)',
                        'borderWidth': 1
                    },
                    {
                        'label': 'Users who Completed All',
                        'data': [d[2] for d in attempt_stats['data']],
                        'backgroundColor': 'rgba(255, 99, 132, 0.5)',
                        'borderColor': 'rgba(255, 99, 132, 1)',
                        'borderWidth': 1
                    }
                ]
            },
            'options': {
                'responsive': True,
                'cutout': '30%',
                'plugins': {
                    'legend': {
                        'position': 'bottom'
                    }
                }
            }
        } 