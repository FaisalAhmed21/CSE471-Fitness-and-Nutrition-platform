"""
Sample Discussion Data Generator
Run this in Django shell: python manage.py shell < create_sample_discussions.py
"""

from django.contrib.auth.models import User
from main.models import Client, Trainer, Discussion, DiscussionReply
from django.utils import timezone
from datetime import timedelta

# Sample discussion data
sample_discussions = [
    {
        "title": "Best pre-workout meal for morning exercises?",
        "tag": "Nutrition",
        "statement": "I usually work out early in the morning around 6 AM. What should I eat before my workout? I've heard conflicting advice about eating before early morning workouts. Some say to eat nothing, others suggest a light snack. What do you recommend for optimal performance?",
    },
    {
        "title": "How many rest days should I take per week?",
        "tag": "Workout",
        "statement": "I'm currently working out 6 days a week doing a mix of cardio and strength training. I'm feeling pretty tired lately. How many rest days do you recommend per week for optimal muscle recovery and growth?",
    },
    {
        "title": "Struggling to lose belly fat despite diet and exercise",
        "tag": "Weight Loss",
        "statement": "I've been following a strict diet and exercising regularly for 3 months now. I've lost some weight overall, but my belly fat doesn't seem to be going away. What am I doing wrong? Any specific exercises or diet changes you'd recommend?",
    },
    {
        "title": "Is protein powder necessary for muscle gain?",
        "tag": "Supplement",
        "statement": "I see everyone at the gym using protein powder. I'm trying to build muscle naturally. Can I achieve good results without supplements by just eating protein-rich foods? Or is protein powder essential for serious gains?",
    },
    {
        "title": "How to stay motivated during weight loss plateau?",
        "tag": "General",
        "statement": "I've been on my weight loss journey for 4 months and lost 15 pounds, but for the last 3 weeks, the scale hasn't moved at all. I'm doing everything the same - same diet, same workouts. How do I push through this plateau? Feeling really discouraged.",
    },
    {
        "title": "Proper deadlift form to avoid back injury",
        "tag": "Workout",
        "statement": "I want to start doing deadlifts but I'm scared of injuring my lower back. Can someone explain the proper form? What are the most common mistakes beginners make with deadlifts?",
    },
    {
        "title": "Bulking diet plan for skinny beginners?",
        "tag": "Muscle Gain",
        "statement": "I'm 6'2\" and weigh only 150 lbs. I want to bulk up and gain muscle mass. What kind of diet should I follow? How many calories should I be eating daily? I have a fast metabolism and find it hard to gain weight.",
    },
]

sample_replies = [
    {
        "discussion_index": 0,
        "reply_text": "For early morning workouts, I recommend eating a small snack 30-45 minutes before. Try half a banana with a tablespoon of peanut butter, or a small bowl of oatmeal. This gives you quick energy without making you feel too full. After your workout, have a proper breakfast with protein and carbs to refuel!",
        "is_solution": True,
    },
    {
        "discussion_index": 1,
        "reply_text": "As a trainer, I typically recommend 1-2 rest days per week, but it depends on your workout intensity. If you're feeling tired, your body is telling you something. Listen to it! Try reducing to 4-5 workout days and see how you feel. Quality over quantity is key.",
        "is_solution": True,
    },
    {
        "discussion_index": 2,
        "reply_text": "Belly fat is often the last to go, unfortunately. Make sure you're getting enough sleep (7-9 hours) and managing stress, as cortisol can contribute to belly fat storage. Also, make sure you're in a calorie deficit and doing a mix of cardio and strength training. Spot reduction is a myth - keep at it and the belly fat will eventually come off!",
        "is_solution": False,
    },
]

def create_sample_data():
    try:
        # Get or create a sample client
        user, created = User.objects.get_or_create(
            username='demo_client',
            defaults={
                'email': 'demo@fitlife.com',
                'first_name': 'John',
                'last_name': 'Doe'
            }
        )
        if created:
            user.set_password('demo123')
            user.save()
        
        client, created = Client.objects.get_or_create(
            user=user,
            defaults={
                'client_usrname': 'demo_client',
                'email': 'demo@fitlife.com',
                'first_name': 'John',
                'last_name': 'Doe'
            }
        )
        
        # Get or create a sample trainer for replies
        trainer_user, created = User.objects.get_or_create(
            username='demo_trainer',
            defaults={
                'email': 'trainer@fitlife.com',
                'first_name': 'Sarah',
                'last_name': 'Johnson'
            }
        )
        if created:
            trainer_user.set_password('demo123')
            trainer_user.save()
        
        trainer, created = Trainer.objects.get_or_create(
            user=trainer_user,
            defaults={
                'trainer_tag': 'DEMO_TR',
                'email': 'trainer@fitlife.com',
                'first_name': 'Sarah',
                'last_name': 'Johnson'
            }
        )
        
        print(f"Using client: {client.client_usrname}")
        print(f"Using trainer: {trainer.trainer_tag}")
        print("\nCreating sample discussions...\n")
        
        # Create discussions
        created_discussions = []
        for i, disc_data in enumerate(sample_discussions):
            discussion = Discussion.objects.create(
                title=disc_data['title'],
                tag=disc_data['tag'],
                statement=disc_data['statement'],
                posted_by=client,
                datetime=timezone.now() - timedelta(days=7-i),  # Spread over last week
                views_count=10 + (i * 5),
                upvotes=i * 2,
            )
            created_discussions.append(discussion)
            print(f"✓ Created: {discussion.title}")
        
        print("\nCreating sample replies...\n")
        
        # Create replies
        for reply_data in sample_replies:
            discussion = created_discussions[reply_data['discussion_index']]
            reply = DiscussionReply.objects.create(
                discussion=discussion,
                reply_text=reply_data['reply_text'],
                replied_by_trainer=trainer,
                datetime=timezone.now() - timedelta(days=6),
                is_solution=reply_data['is_solution']
            )
            
            if reply_data['is_solution']:
                discussion.status = 'resolved'
                discussion.resolved_by = trainer
                discussion.save()
            
            print(f"✓ Created reply for: {discussion.title}")
        
        print("\n" + "="*60)
        print("Sample data created successfully!")
        print("="*60)
        print(f"\nTotal discussions created: {len(created_discussions)}")
        print(f"Total replies created: {len(sample_replies)}")
        print("\nYou can now browse the discussion forum to see these samples.")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    create_sample_data()
