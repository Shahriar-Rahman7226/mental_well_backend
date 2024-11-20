UserRole = (
    ('ADMIN', 'admin'),
    ('COUNSELOR', 'counselor'),
    ('CLIENT', 'client'),
)

PaymentMethodType = (
    ('CASH', 'cash'),
    ('BKASH', 'bkash'),
    # ('BANK', 'bank'),
    # ('NAGAD', 'nagad'),
    # ('ROCKET', 'rocket'),
    # ('VISA', 'visa'),
    # ('MASTER_CARD', 'master_card'),
)

Gender = (
    ('MALE', 'male'),
    ('FEMALE', 'female'),
    ('OTHER', 'other')
)

Days = (
    ('SUNDAY', 'sunday'),
    ('MONDAY', 'monday'),
    ('TUESDAY', 'tuesday'),
    ('WEDNESDAY', 'wednesday'),
    ('THURSDAY', 'thursday'),
    ('FRIDAY', 'friday'),
    ('SATURDAY', 'saturday'),
)

ProfileStatus = (
    ('PENDING', 'pending'),
    ('APPROVED', 'approved'),
    ('REJECTED', 'rejected'),
)

AppointmentStatus = (
    ('PENDING', 'pending'),
    ('ASSIGNED', 'assigned'),
    ('COMPLETED', 'completed'),
    ('CANCELLED', 'cancelled'),
    ('REJECTED', 'rejected'),
)

ScheduleStatus = (
    ('PENDING', 'pending'),
    ('APPROVED', 'approved'),
    ('REJECTED', 'rejected'),
)

ProgressStatus = (
    ('ASSIGNED', 'assigned'),
    ('ONGOING', 'ongoing'),
    ('COMPLETED', 'completed'),
    ('INCOMPLETE', 'incomplete'),
)

ResourceStatus = (
    ('PENDING', 'pending'),
    ('APPROVED', 'approved'),
    ('REJECTED', 'rejected'),
)

ResourceType = (
        ('ARTICLE', 'article'),
        ('VIDEO', 'video'),
        ('AUDIO', 'audio'),
        ('EBOOK', 'ebook'),
        ('RESEARCH PAPER', 'research paper'),
        ('THESIS', 'thesis'),
)

AchievementStatus = (
    ('PENDING', 'pending'),
    ('APPROVED', 'approved'),
    ('REJECTED', 'rejected'),
)